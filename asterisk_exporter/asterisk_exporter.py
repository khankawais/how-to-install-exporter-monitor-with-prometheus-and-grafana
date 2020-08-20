import prometheus_client
import time
import psutil
import subprocess
import os

command_active_channels = "asterisk -rx 'core show channels' | grep 'active channels' | awk '{print $1}'"
command_active_calls = "asterisk -rx 'core show channels' | grep 'active call' | cut -d \   -f 1"
command_calls_processed = "asterisk -rx 'core show channels' | grep 'calls processed' | awk '{print $1}'"
command_sip_peers = "asterisk -rx 'sip show peers' | grep -i 'sip peers \[Monitored:'"


UPDATE_PERIOD = 5
SYSTEM_USAGE = prometheus_client.Gauge('system_usage',
                                       'Hold current system resource usage',
                                       ['resource_type'])

count = prometheus_client.Counter(
    "requests_handled", "Requests Handled by Server")

asterisk_total_active_channels_metric = prometheus_client.Gauge(
    "asterisk_active_channels", "Total current acitve channels")
asterisk_total_active_calls_metric = prometheus_client.Gauge(
    "asterisk_active_calls", "Total current acitve calls")
asterisk_total_calls_processed_metric = prometheus_client.Gauge(
    "asterisk_calls_processed", "Total current calls processed")

asterisk_total_sip_peers_metric = prometheus_client.Gauge(
    "total_sip_peers", "Total SIP Peers")
asterisk_total_online_monitored_sip_peers_metric = prometheus_client.Gauge(
    "total_online_monitored_sip_peers", " Total Online Monitored SIP peers")
asterisk_total_offline_monitored_sip_peers_metric = prometheus_client.Gauge(
    "total_offline_monitored_sip_peers", " Total Offline Monitored SIP peers")
asterisk_total_online_unmonitored_sip_peers_metric = prometheus_client.Gauge(
    "total_online_unmonitored_sip_peers", " Total Online Unmonitored SIP peers")
asterisk_total_offline_unmonitored_sip_peers_metric = prometheus_client.Gauge(
    "total_offline_unmonitored_sip_peers", " Total Offline Unmonitored SIP peers")


if __name__ == '__main__':
prometheus_client.start_http_server(9999)
while True:
    SYSTEM_USAGE.labels('CPU').set(psutil.cpu_percent())
    SYSTEM_USAGE.labels('Memory').set(psutil.virtual_memory()[2])
    count.inc(1)
    asterisk_total_active_channels_metric.set(
        os.popen(command_active_channels).read())
    asterisk_total_active_calls_metric.set(
        os.popen(command_active_calls).read())
    asterisk_total_calls_processed_metric.set(
        os.popen(command_calls_processed).read())
    sip_peers = os.popen(command_sip_peers).read()
    sip = sip_peers.split(" ")
    asterisk_total_sip_peers_metric.set(sip[0])
    asterisk_total_online_monitored_sip_peers_metric.set(sip[4])
    asterisk_total_offline_monitored_sip_peers_metric.set(sip[6])
    asterisk_total_online_unmonitored_sip_peers_metric.set(sip[9])
    asterisk_total_offline_unmonitored_sip_peers_metric.set(sip[11])
    time.sleep(UPDATE_PERIOD)
