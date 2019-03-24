import subprocess
import sys

import xmltodict

PYTHON_MAJOR = sys.version_info[0]

# =========
# Command execution
# =========


def run_command(command):
    """Run a command and return the ouput as a single string"""
    if PYTHON_MAJOR == 3:
        return subprocess.check_output(command + ["-xml"]).decode("utf-8")
    else:
        return subprocess.Popen(
            command + ["-xml"], stdout=subprocess.PIPE
        ).communicate()[0]


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

    jobs = []
    for job in xml["job_info"]["queue_info"]["job_list"]:
        if "tasks" not in job:
            job["tasks"] = ""

        jobs.append(job)
    return jobs


def process_queues_xml(text):
    """Process XML for queues"""
    xml = process_xml(text)
    return xml["job_info"]["cluster_queue_summary"]


# =========
# Getter functions
# =========


def get_hosts():
    """Get dict of host info"""
    # qhost
    # hosts_text = open_file("test/qhost.txt")
    hosts_text = run_command(["qhost"])
    hosts = process_hosts_xml(hosts_text)
    return hosts


def get_jobs():
    """Get dict of job info"""
    # qstat -u "*"
    # jobs_text = open_file("test/jobs.txt")
    jobs_text = run_command(["qstat", "-u", '"*"'])
    jobs = process_jobs_xml(jobs_text)
    return jobs


def get_queues():
    """Get dict of queue info"""
    # qstat -g c
    # queues_text = open_file("test/queue.txt")
    queues_text = run_command(["qstat", "-g", "c"])
    queues = process_queues_xml(queues_text)
    return queues
