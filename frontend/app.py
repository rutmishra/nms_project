import streamlit as st
import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

st.set_page_config(layout="wide")
st.title("📡 Network Monitoring System")

# Tabs for different sections
tab1, tab2 = st.tabs(["System Status", "Device Management"])

# Get backend URL from environment variable
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')

# Configure retry strategy
session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

with tab1:
    # Your existing system status code here
    status_placeholder = st.empty()
    metrics_placeholder = st.empty()

    while True:
        try:
            response = session.get(f"{BACKEND_URL}/api/status/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Update status using placeholder
                with status_placeholder.container():
                    status = data.get("status", "Unknown")
                    if status == "running":
                        st.success("🟢 System Status: Running")
                    else:
                        st.error(f"🔴 System Status: {status}")
                
                # Update metrics using placeholder
                with metrics_placeholder.container():
                    if "system_metrics" in data:
                        metrics = data["system_metrics"]
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("CPU Usage", metrics.get("cpu_usage", "N/A"))
                            st.metric("Memory Usage", metrics.get("memory_usage", "N/A"))
                            st.metric("Memory Available", metrics.get("memory_available", "N/A"))
                        
                        with col2:
                            st.metric("Disk Usage", metrics.get("disk_usage", "N/A"))
                            st.metric("Disk Free", metrics.get("disk_free", "N/A"))
                    
                    st.text(f"Last Updated: {data.get('timestamp', 'N/A')}")
                
            elif response.status_code == 503:
                status_placeholder.error("⚠️ Service is temporarily unavailable")
            else:
                status_placeholder.error(f"⚠️ Error: {response.status_code}")
            
        except requests.exceptions.ConnectionError as e:
            status_placeholder.error("❌ Error: Unable to connect to backend service")
        except requests.exceptions.Timeout as e:
            status_placeholder.error("⏱️ Error: Request to backend timed out")
        except Exception as e:
            status_placeholder.error(f"❌ Error: {str(e)}")

        time.sleep(5)  # Refresh every 5 seconds

with tab2:
    # Device Management
    st.subheader("Device Management")
    
    # Fetch device types for the dropdown
    try:
        device_types_response = session.get(f"{BACKEND_URL}/api/devicetypes/")
        if device_types_response.status_code == 200:
            device_types = device_types_response.json()
            device_type_choices = [dt['name'] for dt in device_types]
        else:
            device_type_choices = ["router", "switch", "server", "firewall", "other"]
    except Exception as e:
        device_type_choices = ["router", "switch", "server", "firewall", "other"]
    
    # Create two columns for Add Device and Device List
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Add New Device")
        # Add New Device Form
        with st.form("add_device"):
            # Basic Information
            st.subheader("Basic Information")
            name = st.text_input("Device Name")
            ip_address = st.text_input("IP Address")
            device_type = st.selectbox("Device Type", device_type_choices)
            location = st.text_input("Location (Optional)")

            # Device Identification
            st.subheader("Device Identification")
            serial_number = st.text_input("Serial Number (Optional)")
            mac_address = st.text_input("MAC Address (Optional)", 
                help="Format: XX:XX:XX:XX:XX:XX")

            # Monitoring Configuration
            st.subheader("Monitoring Configuration")
            probe_type = st.selectbox("Probe Type", ["ICMP (Ping)", "SNMP"])
            
            # Show SNMP credentials only if SNMP is selected
            snmp_credential = None
            if probe_type == "SNMP":
                try:
                    cred_response = session.get(f"{BACKEND_URL}/api/snmpcredentials/")
                    if cred_response.status_code == 200:
                        credentials = cred_response.json()
                        cred_choices = [f"{c['name']} ({c['version']})" for c in credentials]
                        selected_cred = st.selectbox("SNMP Credential", cred_choices)
                        snmp_credential = next(
                            (c['id'] for c in credentials 
                             if f"{c['name']} ({c['version']})" == selected_cred), 
                            None
                        )
                except Exception as e:
                    st.error(f"Error fetching SNMP credentials: {str(e)}")
            
            submit = st.form_submit_button("Add Device")
            
            if submit:
                # Get device type ID
                device_type_id = next(
                    (dt['id'] for dt in device_types if dt['name'] == device_type), 
                    None
                )
                
                if device_type_id:
                    data = {
                        "name": name,
                        "ip_address": ip_address,
                        "device_type": device_type_id,
                        "location": location,
                        "serial_number": serial_number,
                        "mac_address": mac_address,
                        "probe_type": "snmp" if probe_type == "SNMP" else "icmp",
                        "snmp_credential": snmp_credential,
                        "operational_status": "unknown",
                        "is_active": True
                    }
                    try:
                        response = session.post(f"{BACKEND_URL}/api/devices/", json=data)
                        if response.status_code == 201:
                            st.success("Device added successfully!")
                        else:
                            st.error(f"Error adding device: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Invalid device type selected")

    with col2:
        st.markdown("### Device List")
        try:
            response = session.get(f"{BACKEND_URL}/api/devices/")
            if response.status_code == 200:
                devices = response.json()
                
                # Create a table header
                cols = st.columns([2, 2, 1.5, 1.5, 1, 1])
                cols[0].markdown("**Name**")
                cols[1].markdown("**IP Address**")
                cols[2].markdown("**Type**")
                cols[3].markdown("**Monitoring**")
                cols[4].markdown("**Status**")
                cols[5].markdown("**Actions**")
                
                # Create a line separator
                st.markdown("---")
                
                for device in devices:
                    cols = st.columns([2, 2, 1.5, 1.5, 1, 1])
                    
                    # Basic info
                    cols[0].write(f"**{device['name']}**\n{device.get('serial_number', '')}")
                    cols[1].write(f"{device['ip_address']}\n{device.get('mac_address', '')}")
                    cols[2].write(device['device_type_name'])
                    
                    # Monitoring info
                    probe = "SNMP" if device['probe_type'] == 'snmp' else "ICMP"
                    cols[3].write(probe)
                    
                    # Status with icon
                    status = "🟢" if device['operational_status'] == "up" else "🔴"
                    cols[4].write(f"{status} {device['operational_status']}")
                    
                    # Delete button
                    if cols[5].button("Delete", key=device['id']):
                        del_response = session.delete(f"{BACKEND_URL}/api/devices/{device['id']}/")
                        if del_response.status_code == 204:
                            st.success("Device deleted!")
                            st.rerun()
                    
                    # Add a light separator between devices
                    st.markdown("---")
                    
        except Exception as e:
            st.error(f"Error fetching devices: {str(e)}")