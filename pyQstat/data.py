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


def get_queues():
    """Get list of dicts of queue info"""
    if FAKE:
        queues_text = open_file("test/queues.txt")
    else:
        queues_text = run_command(["qstat", "-g", "c"])
    queues = process_queues_xml(queues_text)
    return queues


"""
OrderedDict(
    [
        (
            "job_info",
            OrderedDict(
                [
                    (
                        "@xmlns:xsd",
                        "http://arc.liv.ac.uk/repos/darcs/sge/source/dist/util/resources/schemas/qstat/qstat.xsd",
                    ),
                    (
                        "cluster_queue_summary",
                        OrderedDict(
                            [
                                ("name", "all.q"),
                                ("load", "0.42000"),
                                ("used", "0"),
                                ("resv", "0"),
                                ("available", "0"),
                                ("total", "28"),
                                ("temp_disabled", "0"),
                                ("manual_intervention", "0"),
                            ]
                        ),
                    ),
                ]
            ),
        )
    ]
)
"""
