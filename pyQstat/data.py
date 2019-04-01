import datetime
import os
import subprocess
import sys

import xmltodict

try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote


PYTHON_MAJOR = sys.version_info[0]

FAKE = False
if "FLASK_FAKE" in os.environ.keys():
    FAKE = os.environ["FLASK_FAKE"] == "True"


def sizeof_fmt(num):
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return "%3.2f %s" % (num, x)
        num /= 1024.0


# =========
# Command execution
# =========


def run_command(command):
    """Run a command and return the ouput as a single string"""
    command = command + ["-xml"]

    shell = False
    quotes = ['"', "'"]
    joined = "\t".join(command)

    if any([x in joined for x in quotes]):
        # Python doesn't like the quotations required, so concatentate and run as shell
        shell = True
        command = " ".join(command)

    if PYTHON_MAJOR == 3:
        return subprocess.check_output(command, shell=shell).decode("utf-8")
    else:
        return (
            subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE)
            .communicate()[0]
            .decode("utf-8")
        )


def open_file(filename):
    """Open a file and return the contents as a string"""
    with open(filename, "r") as myfile:
        data = myfile.read()
    return data


# =========
# XML processing
# =========


def process_xml(text):
    """Process XML text into dictionary"""
    return xmltodict.parse(text)


def process_hosts_xml(text):
    """Process XML for hosts, as the structure is very different"""
    xml = process_xml(text)

    if type(xml["qhost"]["host"]) != list:
        return []

    hosts = []
    for host in xml["qhost"]["host"]:
        values = [
            "arch_string",
            "num_proc",
            "m_socket",
            "m_core",
            "m_thread",
            "load_avg",
            "mem_total",
            "mem_used",
            "swap_total",
            "swap_used",
        ]

        new_dict = {"hostname": host["@name"]}
        for i in range(len(values)):
            new_dict[values[i]] = host["hostvalue"][i]["#text"]

        if new_dict["hostname"] != "global":
            # skip the global entry
            hosts.append(new_dict)

    return hosts


def process_jobs_xml(text):
    """Process XML for jobs"""
    xml = process_xml(text)

    if not xml["job_info"]["queue_info"]:
        # will be none if no jobs
        return []

    main_entry = xml["job_info"]["queue_info"]["job_list"]

    jobs = []

    if type(main_entry) == list:
        for job in main_entry:
            if "tasks" not in job:
                job["tasks"] = ""
            jobs.append(job)
    else:
        # single job result will not be in a list
        job = main_entry
        if "tasks" not in job:
            job["tasks"] = ""
        jobs.append(job)

    return jobs


def process_job_xml(text):
    """Process XML for single job"""
    xml = process_xml(text)

    if "unknown_jobs" in xml:
        return ([], [])

    job = xml["detailed_job_info"]["djob_info"]["element"]

    # wrap tasks in a list if not
    if type(job["JB_ja_tasks"]["ulong_sublist"]) != list:
        job["JB_ja_tasks"]["ulong_sublist"] = [job["JB_ja_tasks"]["ulong_sublist"]]

    # fix queue
    if "JB_hard_queue_list" not in job:
        job["JB_hard_queue_list"] = {}
        job["JB_hard_queue_list"]["destin_ident_list"] = {}
        job["JB_hard_queue_list"]["destin_ident_list"]["QR_name"] = ""

    # fix PE
    if "JB_pe" not in job:
        job["JB_pe"] = ""

    # fix pe slots
    if "JB_pe_range" not in job:
        job["JB_pe_range"] = {}
        job["JB_pe_range"]["ranges"] = {}
        job["JB_pe_range"]["RN_Max"] = ""

    # check if messages are present
    if "messages" in xml["detailed_job_info"]:
        messages = xml["detailed_job_info"]["messages"]["element"][
            "SME_global_message_list"
        ]["element"]
        if type(messages) != list:
            messages = [messages]
    else:
        messages = []

    return (job, messages)


def process_queues_xml(text):
    """Process XML for queues"""
    xml = process_xml(text)

    if "cluster_queue_summary" not in xml["job_info"]:
        return []

    queues = xml["job_info"]["cluster_queue_summary"]

    if type(queues) != list:
        # single entry will not be wrapped by list
        queues = [queues]
    return queues


# =========
# Getter functions
# =========


def get_hosts():
    """Get list of dicts of host info"""
    if FAKE:
        hosts_text = open_file("test/hosts.txt")
    else:
        hosts_text = run_command(["qhost"])
    hosts = process_hosts_xml(hosts_text)
    return hosts


def get_jobs(user="*", queue="*"):
    """Get list of dicts of job info"""
    user = cmd_quote(user)
    queue = cmd_quote(queue)

    if FAKE:
        jobs_text = open_file("test/jobs.txt")
    else:
        jobs_text = run_command(["qstat", "-u", user, "-q", queue])
    jobs = process_jobs_xml(jobs_text)
    return jobs


def get_job(id):
    """Get dict of job info"""
    if FAKE:
        job_text = open_file("test/singlejob.txt")
    else:
        job_text = run_command(["qstat", "-j", str(id)])
    job, messages = process_job_xml(job_text)

    if not job:
        return ([], [])

    # convert unix timestamp to local time in a readable format
    ts = int(job["JB_submission_time"])
    new_time = datetime.datetime.fromtimestamp(ts).strftime("%a, %d %b %Y %X %z")
    job["JB_submission_time"] = new_time

    # convert bytes and other unreadable text to human readable
    for task in job["JB_ja_tasks"]["ulong_sublist"]:
        for i, item in enumerate(task["JAT_scaled_usage_list"]["scaled"]):
            value = item["UA_value"]
            if i in [0]:
                value = str(datetime.timedelta(seconds=float(value)))
            elif i in [1]:
                value = "%3.2f GBsec" % (float(value))
            elif i in [2]:
                value = "%3.2f GB" % (float(value))
            elif i in [3]:
                value = "%3.2f sec" % (float(value))
            if i in [4, 5]:
                value = sizeof_fmt(float(value))
            item["UA_value"] = value

    return (job, messages)


def get_queues():
    """Get list of dicts of queue info"""
    if FAKE:
        queues_text = open_file("test/queues.txt")
    else:
        queues_text = run_command(["qstat", "-g", "c"])
    queues = process_queues_xml(queues_text)
    return queues
