"""
Smart Water Tank Level Monitoring and Automatic Pump Control System
Main Module: Real-Time Water Level Monitoring and Automatic Pump Control

This module implements a comprehensive water management system that simulates
real-time water level monitoring, automatic pump control, and overflow/shortage prevention.

Author: Internship Project Team
Date: 2024
"""

import json
import random
import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PumpState(Enum):
    """Pump operational states"""
    ON = "On"
    OFF = "Off"
    STANDBY = "Standby"
    FAULT = "Fault"


class WaterLevel(Enum):
    """Water level status"""
    CRITICAL_LOW = "Critical Low"
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    CRITICAL_HIGH = "Critical High"


class TankType(Enum):
    """Type of water tank"""
    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    INDUSTRIAL = "Industrial"
    INSTITUTIONAL = "Institutional"


@dataclass
class WaterLevelReading:
    """Data class representing water level reading"""
    tank_id: str
    timestamp: datetime.datetime
    water_level: float  # in liters
    water_level_percentage: float  # 0-100%
    water_level_status: WaterLevel
    pump_state: PumpState
    pump_runtime: float  # seconds
    water_usage: float  # liters
    inflow_rate: float  # liters/minute
    outflow_rate: float  # liters/minute
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'tank_id': self.tank_id,
            'timestamp': self.timestamp.isoformat(),
            'water_level': round(self.water_level, 2),
            'water_level_percentage': round(self.water_level_percentage, 2),
            'water_level_status': self.water_level_status.value,
            'pump_state': self.pump_state.value,
            'pump_runtime': round(self.pump_runtime, 2),
            'water_usage': round(self.water_usage, 2),
            'inflow_rate': round(self.inflow_rate, 2),
            'outflow_rate': round(self.outflow_rate, 2)
        }


@dataclass
class PumpControlAction:
    """Data class for pump control action"""
    action_id: str
    tank_id: str
    action_type: str  # 'PUMP_ON', 'PUMP_OFF', 'PUMP_FAULT_DETECTED'
    reason: str
    timestamp: datetime.datetime
    water_level_before: float
    water_level_after: float = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'action_id': self.action_id,
            'tank_id': self.tank_id,
            'action_type': self.action_type,
            'reason': self.reason,
            'timestamp': self.timestamp.isoformat(),
            'water_level_before': round(self.water_level_before, 2),
            'water_level_after': round(self.water_level_after, 2) if self.water_level_after else None
        }


@dataclass
class SystemAlert:
    """Data class representing a system alert"""
    alert_id: str
    tank_id: str
    alert_type: str  # 'OVERFLOW', 'SHORTAGE', 'PUMP_MALFUNCTION', 'SENSOR_FAULT'
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    message: str
    timestamp: datetime.datetime
    resolved: bool = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'tank_id': self.tank_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class WaterTank:
    """Class representing a water tank with monitoring and control"""
    
    def __init__(self, tank_id: str, tank_type: TankType, capacity: float = 1000):
        """
        Initialize a water tank
        
        Args:
            tank_id: Unique tank identifier
            tank_type: Type of tank (Residential, Commercial, Industrial, Institutional)
            capacity: Tank capacity in liters (default 1000L)
        """
        self.tank_id = tank_id
        self.tank_type = tank_type
        self.capacity = capacity
        self.current_level = capacity * 0.5  # Start at 50% capacity
        self.readings: List[WaterLevelReading] = []
        self.alerts: List[SystemAlert] = []
        self.control_actions: List[PumpControlAction] = []
        self.pump_state = PumpState.OFF
        self.pump_runtime_total = 0.0
        self.water_saved = 0.0
        self.last_reading = None
        
        # Thresholds for automatic pump control
        self._set_thresholds()
        
        # Sensor parameters
        self.sensor_accuracy = 0.98  # 98% accuracy
        self.sensor_fault_probability = 0.01  # 1% chance of fault per reading
    
    def _set_thresholds(self):
        """Set water level thresholds based on tank type"""
        if self.tank_type == TankType.RESIDENTIAL:
            self.pump_on_threshold = self.capacity * 0.25  # 25% - Turn pump on
            self.pump_off_threshold = self.capacity * 0.90  # 90% - Turn pump off
            self.critical_low_threshold = self.capacity * 0.10  # 10%
            self.critical_high_threshold = self.capacity * 0.95  # 95%
        elif self.tank_type == TankType.COMMERCIAL:
            self.pump_on_threshold = self.capacity * 0.30
            self.pump_off_threshold = self.capacity * 0.85
            self.critical_low_threshold = self.capacity * 0.15
            self.critical_high_threshold = self.capacity * 0.92
        elif self.tank_type == TankType.INDUSTRIAL:
            self.pump_on_threshold = self.capacity * 0.35
            self.pump_off_threshold = self.capacity * 0.80
            self.critical_low_threshold = self.capacity * 0.20
            self.critical_high_threshold = self.capacity * 0.90
        else:  # INSTITUTIONAL
            self.pump_on_threshold = self.capacity * 0.28
            self.pump_off_threshold = self.capacity * 0.88
            self.critical_low_threshold = self.capacity * 0.12
            self.critical_high_threshold = self.capacity * 0.93
    
    def take_reading(self, hour_of_day: int = 12, peak_usage: bool = False) -> WaterLevelReading:
        """
        Take a water level reading and perform automatic pump control
        
        Args:
            hour_of_day: Hour of the day (0-23)
            peak_usage: Whether it's a peak water usage hour
            
        Returns:
            WaterLevelReading object
        """
        timestamp = datetime.datetime.now()
        
        # Generate water usage based on time of day and tank type
        if peak_usage or (7 <= hour_of_day < 9) or (18 <= hour_of_day < 20):
            # Peak usage hours
            if self.tank_type == TankType.RESIDENTIAL:
                water_usage = random.uniform(50, 100)
            elif self.tank_type == TankType.COMMERCIAL:
                water_usage = random.uniform(150, 300)
            elif self.tank_type == TankType.INDUSTRIAL:
                water_usage = random.uniform(300, 500)
            else:  # INSTITUTIONAL
                water_usage = random.uniform(200, 400)
        else:
            # Off-peak usage
            if self.tank_type == TankType.RESIDENTIAL:
                water_usage = random.uniform(10, 40)
            elif self.tank_type == TankType.COMMERCIAL:
                water_usage = random.uniform(30, 80)
            elif self.tank_type == TankType.INDUSTRIAL:
                water_usage = random.uniform(50, 150)
            else:  # INSTITUTIONAL
                water_usage = random.uniform(40, 100)
        
        # Simulate water outflow
        self.current_level -= water_usage
        self.current_level = max(0, self.current_level)
        
        # Automatic pump control logic
        self._control_pump()
        
        # Simulate water inflow if pump is on
        if self.pump_state == PumpState.ON:
            pump_inflow = self._calculate_pump_inflow()
            self.current_level += pump_inflow
            self.pump_runtime_total += 1  # Increment by 1 minute
        else:
            pump_inflow = 0
        
        # Ensure level doesn't exceed capacity
        if self.current_level > self.capacity:
            self.current_level = self.capacity
        
        # Calculate percentages and status
        water_level_percentage = (self.current_level / self.capacity) * 100
        water_level_status = self._classify_water_level(water_level_percentage)
        
        # Create reading with sensor accuracy applied
        sensor_reading = self.current_level * self.sensor_accuracy + random.uniform(-5, 5)
        sensor_reading = max(0, min(self.capacity, sensor_reading))
        
        reading = WaterLevelReading(
            tank_id=self.tank_id,
            timestamp=timestamp,
            water_level=sensor_reading,
            water_level_percentage=water_level_percentage,
            water_level_status=water_level_status,
            pump_state=self.pump_state,
            pump_runtime=self.pump_runtime_total,
            water_usage=water_usage,
            inflow_rate=pump_inflow,
            outflow_rate=water_usage
        )
        
        self.readings.append(reading)
        self.last_reading = reading
        
        # Check for anomalies and generate alerts
        self._detect_anomalies(reading, water_level_percentage)
        
        return reading
    
    def _control_pump(self):
        """Automatic pump control based on water level"""
        if self.pump_state == PumpState.FAULT:
            return  # Don't control if pump is faulty
        
        # Turn pump on if water level is too low
        if self.current_level <= self.pump_on_threshold and self.pump_state == PumpState.OFF:
            self.pump_state = PumpState.ON
            action = PumpControlAction(
                action_id=f"ACTION_{len(self.control_actions) + 1}",
                tank_id=self.tank_id,
                action_type="PUMP_ON",
                reason=f"Water level ({self.current_level:.1f}L) below threshold ({self.pump_on_threshold:.1f}L)",
                timestamp=datetime.datetime.now(),
                water_level_before=self.current_level
            )
            self.control_actions.append(action)
            logger.info(f"Pump ON for {self.tank_id}: Water level {self.current_level:.1f}L")
        
        # Turn pump off if water level is sufficient
        elif self.current_level >= self.pump_off_threshold and self.pump_state == PumpState.ON:
            self.pump_state = PumpState.OFF
            action = PumpControlAction(
                action_id=f"ACTION_{len(self.control_actions) + 1}",
                tank_id=self.tank_id,
                action_type="PUMP_OFF",
                reason=f"Water level ({self.current_level:.1f}L) above threshold ({self.pump_off_threshold:.1f}L)",
                timestamp=datetime.datetime.now(),
                water_level_before=self.current_level
            )
            self.control_actions.append(action)
            logger.info(f"Pump OFF for {self.tank_id}: Water level {self.current_level:.1f}L")
    
    def _calculate_pump_inflow(self) -> float:
        """Calculate water inflow from pump"""
        if self.tank_type == TankType.RESIDENTIAL:
            return random.uniform(15, 25)  # liters/minute
        elif self.tank_type == TankType.COMMERCIAL:
            return random.uniform(40, 60)
        elif self.tank_type == TankType.INDUSTRIAL:
            return random.uniform(80, 120)
        else:  # INSTITUTIONAL
            return random.uniform(60, 100)
    
    def _classify_water_level(self, percentage: float) -> WaterLevel:
        """Classify water level based on percentage"""
        if percentage <= 10:
            return WaterLevel.CRITICAL_LOW
        elif percentage <= 25:
            return WaterLevel.LOW
        elif percentage <= 75:
            return WaterLevel.NORMAL
        elif percentage <= 90:
            return WaterLevel.HIGH
        else:
            return WaterLevel.CRITICAL_HIGH
    
    def _detect_anomalies(self, reading: WaterLevelReading, percentage: float):
        """Detect anomalies and generate alerts"""
        # Check for critical low level
        if percentage <= 10:
            alert = SystemAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                tank_id=self.tank_id,
                alert_type="SHORTAGE",
                severity="CRITICAL",
                message=f"Critical water shortage: Tank level at {percentage:.1f}%",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.critical(f"CRITICAL: Water shortage in {self.tank_id}")
        
        # Check for critical high level (overflow risk)
        elif percentage >= 95:
            alert = SystemAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                tank_id=self.tank_id,
                alert_type="OVERFLOW",
                severity="HIGH",
                message=f"Overflow risk: Tank level at {percentage:.1f}%",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.warning(f"WARNING: Overflow risk in {self.tank_id}")
        
        # Check for sensor faults
        if random.random() < self.sensor_fault_probability:
            alert = SystemAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                tank_id=self.tank_id,
                alert_type="SENSOR_FAULT",
                severity="MEDIUM",
                message="Sensor fault detected - accuracy compromised",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.warning(f"Sensor fault detected in {self.tank_id}")
        
        # Check for pump malfunction (if pump should be on but water level not increasing)
        if len(self.readings) >= 2:
            prev_reading = self.readings[-2]
            if (self.pump_state == PumpState.ON and 
                reading.water_level < prev_reading.water_level and
                reading.water_level > 0):
                alert = SystemAlert(
                    alert_id=f"ALERT_{len(self.alerts) + 1}",
                    tank_id=self.tank_id,
                    alert_type="PUMP_MALFUNCTION",
                    severity="HIGH",
                    message="Pump malfunction: Water level decreasing despite pump being ON",
                    timestamp=datetime.datetime.now()
                )
                self.alerts.append(alert)
                logger.warning(f"Pump malfunction detected in {self.tank_id}")
    
    def get_tank_status(self) -> Dict:
        """Get current tank status"""
        return {
            'tank_id': self.tank_id,
            'tank_type': self.tank_type.value,
            'capacity': self.capacity,
            'current_level': round(self.current_level, 2),
            'level_percentage': round((self.current_level / self.capacity) * 100, 2),
            'pump_state': self.pump_state.value,
            'pump_runtime_total': round(self.pump_runtime_total, 2),
            'total_alerts': len(self.alerts),
            'active_alerts': len([a for a in self.alerts if not a.resolved]),
            'last_reading': self.last_reading.to_dict() if self.last_reading else None
        }
    
    def get_efficiency_metrics(self) -> Dict:
        """Calculate efficiency metrics"""
        if len(self.readings) == 0:
            return {}
        
        total_usage = sum(r.water_usage for r in self.readings)
        avg_level = sum(r.water_level_percentage for r in self.readings) / len(self.readings)
        overflow_count = len([a for a in self.alerts if a.alert_type == "OVERFLOW"])
        shortage_count = len([a for a in self.alerts if a.alert_type == "SHORTAGE"])
        
        return {
            'total_water_usage': round(total_usage, 2),
            'average_level_percentage': round(avg_level, 2),
            'overflow_incidents': overflow_count,
            'shortage_incidents': shortage_count,
            'pump_efficiency': round((self.pump_runtime_total / len(self.readings)) * 100, 2),
            'water_saved_by_prevention': round(self.water_saved, 2)
        }


class WaterManagementSystem:
    """System managing multiple water tanks"""
    
    def __init__(self):
        """Initialize water management system"""
        self.tanks: Dict[str, WaterTank] = {}
        self.all_alerts: List[SystemAlert] = []
        self.operation_log: List[Dict] = []
        
        self._initialize_tanks()
        logger.info(f"Water Management System initialized with {len(self.tanks)} tanks")
    
    def _initialize_tanks(self):
        """Initialize tanks for different facility types"""
        tank_configs = [
            ("TANK_RES_001", TankType.RESIDENTIAL, 1000),
            ("TANK_COM_001", TankType.COMMERCIAL, 5000),
            ("TANK_IND_001", TankType.INDUSTRIAL, 10000),
            ("TANK_INST_001", TankType.INSTITUTIONAL, 3000)
        ]
        
        for tank_id, tank_type, capacity in tank_configs:
            tank = WaterTank(tank_id, tank_type, capacity)
            self.tanks[tank_id] = tank
    
    def read_all_tanks(self, hour_of_day: int = 12, peak_usage: bool = False):
        """Read all tanks in the system"""
        for tank_id, tank in self.tanks.items():
            reading = tank.take_reading(hour_of_day, peak_usage)
            
            # Collect alerts
            for alert in tank.alerts:
                if not alert.resolved:
                    self.all_alerts.append(alert)
    
    def get_system_statistics(self) -> Dict:
        """Get system-wide statistics"""
        total_tanks = len(self.tanks)
        total_capacity = sum(tank.capacity for tank in self.tanks.values())
        total_current_level = sum(tank.current_level for tank in self.tanks.values())
        
        # Count tank status
        tank_status_distribution = {}
        for tank in self.tanks.values():
            if tank.last_reading:
                status = tank.last_reading.water_level_status.value
                tank_status_distribution[status] = tank_status_distribution.get(status, 0) + 1
        
        return {
            'total_tanks': total_tanks,
            'total_capacity': round(total_capacity, 2),
            'total_current_level': round(total_current_level, 2),
            'system_fill_percentage': round((total_current_level / total_capacity) * 100, 2),
            'tank_status_distribution': tank_status_distribution,
            'active_alerts': len([a for a in self.all_alerts if not a.resolved]),
            'pumps_running': len([t for t in self.tanks.values() if t.pump_state == PumpState.ON])
        }
    
    def get_hourly_report(self) -> Dict:
        """Generate hourly monitoring report"""
        stats = self.get_system_statistics()
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'statistics': stats,
            'tank_details': {tank_id: tank.get_tank_status() for tank_id, tank in self.tanks.items()}
        }
        
        self.operation_log.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'system_fill_percentage': stats['system_fill_percentage'],
            'active_alerts': stats['active_alerts'],
            'pumps_running': stats['pumps_running']
        })
        
        return report
    
    def export_to_json(self, filename: str):
        """Export system data to JSON"""
        data = {
            'system_name': 'Smart Water Tank Management System',
            'total_tanks': len(self.tanks),
            'tanks': {tank_id: tank.get_tank_status() for tank_id, tank in self.tanks.items()},
            'alerts': [alert.to_dict() for alert in self.all_alerts],
            'operation_log': self.operation_log
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Data exported to {filename}")


class WaterSimulator:
    """Simulator for generating realistic water usage scenarios"""
    
    def __init__(self, system: WaterManagementSystem):
        """Initialize simulator"""
        self.system = system
    
    def simulate_24_hour_cycle(self, peak_hours: List[int] = None):
        """
        Simulate a full 24-hour water usage cycle
        
        Args:
            peak_hours: List of hours when peak usage occurs
        """
        if peak_hours is None:
            peak_hours = [7, 8, 18, 19]  # Morning and evening peak usage
        
        logger.info("Starting 24-hour water management simulation")
        
        for hour in range(24):
            peak_usage = hour in peak_hours
            
            # Read all tanks
            self.system.read_all_tanks(hour_of_day=hour, peak_usage=peak_usage)
            
            # Generate hourly report
            report = self.system.get_hourly_report()
            
            logger.info(f"Hour {hour:02d}:00 - Fill: {report['statistics']['system_fill_percentage']:.1f}%, "
                       f"Alerts: {report['statistics']['active_alerts']}, "
                       f"Pumps Running: {report['statistics']['pumps_running']}")
        
        logger.info("24-hour simulation completed")
    
    def get_simulation_report(self) -> Dict:
        """Get comprehensive simulation report"""
        return self.system.get_hourly_report()


if __name__ == "__main__":
    # Create water management system
    system = WaterManagementSystem()
    
    # Create simulator
    simulator = WaterSimulator(system)
    
    # Run simulation with peak hours
    simulator.simulate_24_hour_cycle(peak_hours=[7, 8, 18, 19])
    
    # Generate report
    report = simulator.get_simulation_report()
    
    # Print report
    print("\n" + "="*60)
    print("SMART WATER TANK MANAGEMENT SYSTEM - SIMULATION REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))
    
    # Export data
    system.export_to_json('/home/ubuntu/water_tank_system_data.json')
