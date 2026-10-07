"""
IoT Sensor Simulation Module for Water Tank System

This module simulates IoT-based sensors (ultrasonic, pressure, temperature) used for
intelligent water level monitoring. It includes sensor data generation, anomaly detection,
and alert generation.

Author: Internship Project Team
Date: 2024
"""

import random
import datetime
import json
import logging
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SensorType(Enum):
    """Types of sensors used in water level detection"""
    ULTRASONIC = "Ultrasonic"
    PRESSURE = "Pressure"
    FLOAT_SWITCH = "Float Switch"
    CAPACITIVE = "Capacitive"


class SensorStatus(Enum):
    """Status of sensor"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    FAULTY = "Faulty"
    MAINTENANCE = "Maintenance"


@dataclass
class WaterLevelSensorReading:
    """Data class for water level sensor reading"""
    sensor_id: str
    timestamp: datetime.datetime
    water_level: float  # in liters
    level_percentage: float  # 0-100%
    sensor_type: SensorType
    tank_id: str
    status: SensorStatus
    confidence: float  # 0.0 to 1.0
    temperature: float  # Celsius
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp.isoformat(),
            'water_level': round(self.water_level, 2),
            'level_percentage': round(self.level_percentage, 2),
            'sensor_type': self.sensor_type.value,
            'tank_id': self.tank_id,
            'status': self.status.value,
            'confidence': round(self.confidence, 3),
            'temperature': round(self.temperature, 1)
        }


@dataclass
class SensorAlert:
    """Data class for sensor alert"""
    alert_id: str
    sensor_id: str
    alert_type: str  # 'MALFUNCTION', 'LOW_CONFIDENCE', 'CALIBRATION_NEEDED', 'BATTERY_LOW'
    severity: str  # 'LOW', 'MEDIUM', 'HIGH'
    message: str
    timestamp: datetime.datetime
    resolved: bool = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'sensor_id': self.sensor_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class IoTWaterLevelSensor:
    """Base class for IoT water level sensors"""
    
    def __init__(self, sensor_id: str, sensor_type: SensorType, tank_id: str, tank_capacity: float):
        """Initialize sensor"""
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.tank_id = tank_id
        self.tank_capacity = tank_capacity
        self.status = SensorStatus.ACTIVE
        self.last_reading = None
        self.readings_history: List[WaterLevelSensorReading] = []
        self.alerts: List[SensorAlert] = []
        self.calibration_needed = False
        self.battery_level = 100.0  # Battery percentage
        self.total_readings = 0
        self.sensor_accuracy = self._get_sensor_accuracy()
    
    def _get_sensor_accuracy(self) -> float:
        """Get sensor accuracy based on type"""
        if self.sensor_type == SensorType.ULTRASONIC:
            return 0.95  # 95% accuracy
        elif self.sensor_type == SensorType.PRESSURE:
            return 0.98  # 98% accuracy
        elif self.sensor_type == SensorType.FLOAT_SWITCH:
            return 0.99  # 99% accuracy
        else:  # CAPACITIVE
            return 0.96  # 96% accuracy
    
    def take_reading(self, actual_level: float, temperature: float = 25.0) -> WaterLevelSensorReading:
        """
        Take a water level reading
        
        Args:
            actual_level: Actual water level in liters
            temperature: Water temperature in Celsius
            
        Returns:
            WaterLevelSensorReading object
        """
        timestamp = datetime.datetime.now()
        
        # Apply sensor accuracy and add noise
        measured_level = actual_level * self.sensor_accuracy + random.uniform(-10, 10)
        measured_level = max(0, min(self.tank_capacity, measured_level))
        
        # Calculate percentage
        level_percentage = (measured_level / self.tank_capacity) * 100
        
        # Calculate confidence based on sensor conditions
        confidence = self._calculate_confidence(temperature)
        
        # Create reading object
        reading = WaterLevelSensorReading(
            sensor_id=self.sensor_id,
            timestamp=timestamp,
            water_level=measured_level,
            level_percentage=level_percentage,
            sensor_type=self.sensor_type,
            tank_id=self.tank_id,
            status=self.status,
            confidence=confidence,
            temperature=temperature
        )
        
        self.last_reading = reading
        self.readings_history.append(reading)
        self.total_readings += 1
        
        # Simulate battery drain
        self.battery_level -= random.uniform(0.02, 0.05)
        
        # Check for anomalies
        self._check_anomalies(reading)
        
        return reading
    
    def _calculate_confidence(self, temperature: float) -> float:
        """Calculate confidence score for the reading"""
        base_confidence = self.sensor_accuracy
        
        # Reduce confidence if temperature is extreme
        if temperature < 0 or temperature > 60:
            base_confidence *= 0.8
        
        # Reduce confidence if battery is low
        if self.battery_level < 20:
            base_confidence *= 0.7
        elif self.battery_level < 50:
            base_confidence *= 0.85
        
        # Reduce confidence if sensor needs calibration
        if self.calibration_needed:
            base_confidence *= 0.6
        
        # Reduce confidence if sensor is faulty
        if self.status == SensorStatus.FAULTY:
            base_confidence *= 0.3
        
        return max(0.0, min(1.0, base_confidence))
    
    def _check_anomalies(self, reading: WaterLevelSensorReading):
        """Check for sensor anomalies"""
        if len(self.readings_history) < 2:
            return
        
        prev_reading = self.readings_history[-2]
        
        # Check for unrealistic jumps
        level_change = abs(reading.water_level - prev_reading.water_level)
        
        if level_change > self.tank_capacity * 0.3:  # More than 30% change in one reading
            alert = SensorAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                alert_type="MALFUNCTION",
                severity="MEDIUM",
                message=f"Unrealistic level change: {prev_reading.water_level:.1f}L -> {reading.water_level:.1f}L",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
        
        # Check low confidence
        if reading.confidence < 0.5:
            alert = SensorAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                alert_type="LOW_CONFIDENCE",
                severity="MEDIUM",
                message=f"Low reading confidence: {reading.confidence:.2f}",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
        
        # Check battery level
        if self.battery_level < 10:
            alert = SensorAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                alert_type="BATTERY_LOW",
                severity="HIGH",
                message=f"Battery level critical: {self.battery_level:.1f}%",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
        
        # Check for temperature extremes
        if reading.temperature < 0 or reading.temperature > 60:
            alert = SensorAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                alert_type="MALFUNCTION",
                severity="MEDIUM",
                message=f"Temperature out of range: {reading.temperature:.1f}°C",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
    
    def calibrate(self):
        """Calibrate sensor"""
        self.calibration_needed = False
        logger.info(f"Sensor {self.sensor_id} calibrated successfully")
    
    def perform_maintenance(self):
        """Perform maintenance on sensor"""
        self.status = SensorStatus.ACTIVE
        self.battery_level = 100.0
        self.calibration_needed = False
        logger.info(f"Maintenance completed for sensor {self.sensor_id}")
    
    def get_health_status(self) -> Dict:
        """Get sensor health status"""
        return {
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type.value,
            'tank_id': self.tank_id,
            'status': self.status.value,
            'battery_level': round(self.battery_level, 2),
            'calibration_needed': self.calibration_needed,
            'last_reading': self.last_reading.to_dict() if self.last_reading else None,
            'total_readings': self.total_readings,
            'active_alerts': len([a for a in self.alerts if not a.resolved])
        }


class SensorNetworkWater:
    """Network of IoT sensors for the water tank system"""
    
    def __init__(self, tanks: Dict):
        """Initialize sensor network"""
        self.tanks = tanks
        self.sensors: Dict[str, IoTWaterLevelSensor] = {}
        self.all_readings: List[WaterLevelSensorReading] = []
        self.all_alerts: List[SensorAlert] = []
        
        self._initialize_sensors()
    
    def _initialize_sensors(self):
        """Initialize sensors for all tanks"""
        sensor_types = [SensorType.ULTRASONIC, SensorType.PRESSURE, SensorType.FLOAT_SWITCH]
        
        for tank_id, tank in self.tanks.items():
            for i, sensor_type in enumerate(sensor_types):
                sensor_id = f"SENSOR_{tank_id}_{sensor_type.value.replace(' ', '_')}"
                sensor = IoTWaterLevelSensor(sensor_id, sensor_type, tank_id, tank.capacity)
                self.sensors[sensor_id] = sensor
        
        logger.info(f"Initialized {len(self.sensors)} sensors for water tank network")
    
    def read_all_sensors(self, tanks: Dict, temperature: float = 25.0):
        """Read all sensors in the network"""
        for tank_id, tank in tanks.items():
            for sensor_id, sensor in self.sensors.items():
                if sensor.tank_id == tank_id:
                    # Take reading
                    reading = sensor.take_reading(tank.current_level, temperature)
                    self.all_readings.append(reading)
                    
                    # Collect alerts
                    for alert in sensor.alerts:
                        if not alert.resolved:
                            self.all_alerts.append(alert)
    
    def get_network_health(self) -> Dict:
        """Get overall network health"""
        active_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.ACTIVE)
        faulty_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.FAULTY)
        low_battery_sensors = sum(1 for s in self.sensors.values() if s.battery_level < 20)
        
        return {
            'total_sensors': len(self.sensors),
            'active_sensors': active_sensors,
            'faulty_sensors': faulty_sensors,
            'low_battery_sensors': low_battery_sensors,
            'network_health_percentage': round((active_sensors / len(self.sensors)) * 100, 2),
            'total_readings': len(self.all_readings),
            'active_alerts': len([a for a in self.all_alerts if not a.resolved])
        }
    
    def get_sensor_status_report(self) -> Dict:
        """Get detailed sensor status report"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'network_health': self.get_network_health(),
            'sensor_details': [sensor.get_health_status() for sensor in self.sensors.values()],
            'recent_alerts': [alert.to_dict() for alert in self.all_alerts[-10:]]  # Last 10 alerts
        }
        return report
    
    def export_readings(self, filename: str):
        """Export all sensor readings to JSON"""
        data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'total_readings': len(self.all_readings),
            'readings': [reading.to_dict() for reading in self.all_readings[-100:]],  # Last 100 readings
            'alerts': [alert.to_dict() for alert in self.all_alerts],
            'network_health': self.get_network_health()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Sensor readings exported to {filename}")


if __name__ == "__main__":
    from water_tank_system import WaterManagementSystem, WaterSimulator
    
    # Create system
    system = WaterManagementSystem()
    
    # Run simulation
    simulator = WaterSimulator(system)
    simulator.simulate_24_hour_cycle()
    
    # Create sensor network
    sensor_network = SensorNetworkWater(system.tanks)
    
    # Read all sensors
    for hour in range(24):
        peak_usage = hour in [7, 8, 18, 19]
        sensor_network.read_all_sensors(system.tanks, temperature=20 + random.uniform(-5, 5))
    
    # Get report
    report = sensor_network.get_sensor_status_report()
    print(json.dumps(report, indent=2))
    
    # Export data
    sensor_network.export_readings('/home/ubuntu/water_sensor_readings.json')
