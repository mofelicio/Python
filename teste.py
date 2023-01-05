import pandas as pd
import streamlit as st
from pyModbusTCP.client import ModbusClient

st.set_page_config(page_title='Quarto 201')

SetP = st.slider('Setpoint de temperatura', 19, 24, 27)
st.write(SetP)

# init modbus client
c = ModbusClient(debug=False, auto_open=True)
regs_l = c.write_single_register(0, SetP)