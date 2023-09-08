#!/usr/bin/env python3
import argparse
import inspect
import os
import select
import sys

from artiq.experiment import *
from artiq.master.databases import DeviceDB
from artiq.master.worker_db import DeviceManager
from artiq.coredevice.rtio import rtio_output
from artiq.coredevice.shuttler import Config, Volt, Dds, Trigger

class IdleKernel(EnvExperiment):
    def build(self):
        self.setattr_device("core")

        self.leds = dict()
        self.ttl_outs = dict()
        
        self.dacs_config = dict()
        self.dac_volt = dict()
        self.dac_dds = dict()
        self.dac_trigger = dict()
        
        ddb = self.get_device_db()
        for name, desc in ddb.items():
            if isinstance(desc, dict) and desc["type"] == "local":
                module, cls = desc["module"], desc["class"]
                if (module, cls) == ("artiq.coredevice.ttl", "TTLOut"):
                    dev = self.get_device(name)
                    if "led" in name: 
                        self.leds[name] = dev
                    else:
                        self.ttl_outs[name] = dev
                
                if (module, cls) == ("artiq.coredevice.shuttler", "Config"):
                    dev = self.get_device(name)
                    self.dacs_config[name] = dev

                if (module, cls) == ("artiq.coredevice.shuttler", "Volt"):
                    dev = self.get_device(name)
                    self.dac_volt[name] = dev
                
                if (module, cls) == ("artiq.coredevice.shuttler", "Dds"):
                    dev = self.get_device(name)
                    self.dac_dds[name] = dev
                
                if (module, cls) == ("artiq.coredevice.shuttler", "Trigger"):
                    dev = self.get_device(name)
                    self.dac_trigger[name] = dev
                
        
        self.leds = sorted(self.leds.items(), key=lambda x: x[1].channel)
        self.ttl_outs = sorted(self.ttl_outs.items(), key=lambda x: x[1].channel)

        self.dacs_config = sorted(self.dacs_config.items(), key=lambda x: x[1].channel)
        self.dac_volt = sorted(self.dac_volt.items(), key=lambda x: x[1].channel)
        self.dac_dds = sorted(self.dac_dds.items(), key=lambda x: x[1].channel)
        self.dac_trigger = sorted(self.dac_trigger.items(), key=lambda x: x[1].channel)
        

    @kernel
    def set_dac_config(self, config):
        config.set_config(0xFFFF)

    @kernel
    def set_test_dac_volt(self, volt):
        a0 = 0
        a1 = 0
        a2 = 0
        a3 = 0
        volt.set_waveform(a0, a1, a2, a3)


    @kernel
    def set_test_dac_dds(self, dds):
        b0 = 0x0FFF 
        b1 = 0
        b2 = 0
        b3 = 0
        c0 = 0
        c1 = 0x147AE148 # Frequency = 10MHz
        c2 = 0
        dds.set_waveform(b0, b1, b2, b3, c0, c1, c2)
    
    @kernel
    def set_dac_trigger(self, trigger):
        trigger.trigger(0xFFFF)

    @kernel
    def run(self):
        self.core.reset()

        self.core.break_realtime()
        t = now_mu() - self.core.seconds_to_mu(0.2)
        while self.core.get_rtio_counter_mu() < t:
            pass

        for dac_config_name, dac_config_dev in self.dacs_config:
            self.set_dac_config(dac_config_dev)

        for dac_volt_name, dac_volt_dev in self.dac_volt:
            self.set_test_dac_volt(dac_volt_dev)

        for dac_dds_name, dac_dds_dev in self.dac_dds:
            self.set_test_dac_dds(dac_dds_dev) 

        for dac_trigger_name, dac_trigger_dev in self.dac_trigger:
             self.set_dac_trigger(dac_trigger_dev)

        print("Configurations are loaded.")

def main():
    device_mgr = DeviceManager(DeviceDB("device_db.py"))
    try:
        experiment = IdleKernel((device_mgr, None, None, None))
        experiment.prepare()
        experiment.run()
        experiment.analyze()
    finally:
        device_mgr.close_devices()

if __name__ == "__main__":
    main()
