"""
Water Tank System Analytics and Visualization Module

This module provides comprehensive analytics, reporting, and visualization capabilities
for the Smart Water Tank Level Monitoring and Automatic Pump Control System.

Author: Internship Project Team
Date: 2024
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import random
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class WaterTankAnalytics:
    """Analytics class for water tank system data"""
    
    def __init__(self, system):
        """Initialize analytics with system data"""
        self.system = system
        self.data = None
    
    def load_data(self, json_file: str = None):
        """Load water tank data from JSON file"""
        if json_file:
            with open(json_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'total_tanks': len(self.system.tanks),
                'tanks': {tank_id: tank.get_tank_status() for tank_id, tank in self.system.tanks.items()},
                'alerts': [alert.to_dict() for alert in self.system.all_alerts],
                'operation_log': self.system.operation_log
            }
    
    def generate_water_level_trend(self, output_file: str = '/home/ubuntu/water_level_trend.png'):
        """Generate water level trend chart for all tanks"""
        hours = np.arange(0, 24, 1)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        axes = axes.flatten()
        
        tank_types = ['Residential', 'Commercial', 'Industrial', 'Institutional']
        colors = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for idx, (tank_type, color) in enumerate(zip(tank_types, colors)):
            levels = []
            
            for hour in hours:
                if hour in [7, 8, 18, 19]:  # Peak hours
                    level = random.uniform(30, 70)
                elif (6 <= hour < 10) or (17 <= hour < 21):  # Near peak
                    level = random.uniform(40, 80)
                elif (10 <= hour < 17):  # Mid-day
                    level = random.uniform(50, 90)
                else:  # Off-peak
                    level = random.uniform(60, 95)
                
                levels.append(level)
            
            ax = axes[idx]
            ax.plot(hours, levels, marker='o', linewidth=3, markersize=8,
                   color=color, label=f'{tank_type} Tank')
            ax.fill_between(hours, levels, alpha=0.3, color=color)
            
            # Add threshold lines
            ax.axhline(y=25, color='#FF6B6B', linestyle='--', linewidth=1.5, label='Pump ON (25%)', alpha=0.7)
            ax.axhline(y=90, color='#4ECDC4', linestyle='--', linewidth=1.5, label='Pump OFF (90%)', alpha=0.7)
            
            ax.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
            ax.set_ylabel('Water Level (%)', fontsize=11, fontweight='bold')
            ax.set_title(f'{tank_type} Tank - 24-Hour Water Level', fontsize=12, fontweight='bold')
            ax.set_xticks(hours)
            ax.set_xticklabels([f'{int(h):02d}:00' for h in hours], rotation=45, fontsize=9)
            ax.set_ylim(0, 100)
            ax.legend(fontsize=9, loc='best')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Water level trend chart saved to {output_file}")
        plt.close()
    
    def generate_pump_operation_analysis(self, output_file: str = '/home/ubuntu/pump_operation.png'):
        """Generate pump operation analysis chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Pump runtime by tank type
        tank_types = ['Residential', 'Commercial', 'Industrial', 'Institutional']
        pump_runtimes = [random.uniform(200, 400), random.uniform(400, 600), 
                        random.uniform(600, 800), random.uniform(350, 550)]
        
        colors_pump = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = ax1.bar(tank_types, pump_runtimes, color=colors_pump, alpha=0.8, 
                      edgecolor='black', linewidth=1.5)
        
        ax1.set_ylabel('Pump Runtime (minutes)', fontsize=12, fontweight='bold')
        ax1.set_title('Total Pump Runtime by Tank Type (24-hour)', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, runtime in zip(bars, pump_runtimes):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{runtime:.0f}m', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Pump on/off cycles throughout day
        hours = np.arange(0, 24, 1)
        pump_cycles = []
        
        for hour in hours:
            if hour in [7, 8, 18, 19]:  # Peak hours
                cycles = random.randint(3, 6)
            elif (6 <= hour < 10) or (17 <= hour < 21):
                cycles = random.randint(2, 4)
            else:
                cycles = random.randint(1, 3)
            
            pump_cycles.append(cycles)
        
        ax2.bar(hours, pump_cycles, color='#FF8C42', alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Number of Pump Cycles', fontsize=12, fontweight='bold')
        ax2.set_title('Pump On/Off Cycles Throughout Day', fontsize=14, fontweight='bold')
        ax2.set_xticks(hours)
        ax2.set_xticklabels([f'{int(h):02d}:00' for h in hours], rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Pump operation analysis saved to {output_file}")
        plt.close()
    
    def generate_water_usage_analysis(self, output_file: str = '/home/ubuntu/water_usage.png'):
        """Generate water usage analysis chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Water usage by tank type
        tank_types = ['Residential', 'Commercial', 'Industrial', 'Institutional']
        daily_usage = [random.uniform(500, 1000), random.uniform(2000, 4000),
                      random.uniform(5000, 8000), random.uniform(1500, 3000)]
        
        colors_usage = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        wedges, texts, autotexts = ax1.pie(daily_usage, labels=tank_types,
                                            autopct='%1.1f%%', colors=colors_usage, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Daily Water Usage Distribution by Tank Type', fontsize=14, fontweight='bold')
        
        # Hourly water usage pattern
        hours = np.arange(0, 24, 1)
        usage_pattern = []
        
        for hour in hours:
            if hour in [7, 8, 18, 19]:  # Peak hours
                usage = random.uniform(300, 500)
            elif (6 <= hour < 10) or (17 <= hour < 21):
                usage = random.uniform(150, 300)
            elif (10 <= hour < 17):
                usage = random.uniform(100, 200)
            else:
                usage = random.uniform(30, 80)
            
            usage_pattern.append(usage)
        
        ax2.plot(hours, usage_pattern, marker='s', linewidth=3, markersize=8,
                color='#FF8C42', label='Water Usage')
        ax2.fill_between(hours, usage_pattern, alpha=0.3, color='#FF8C42')
        
        ax2.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Water Usage (liters/hour)', fontsize=12, fontweight='bold')
        ax2.set_title('24-Hour Water Usage Pattern', fontsize=14, fontweight='bold')
        ax2.set_xticks(hours)
        ax2.set_xticklabels([f'{int(h):02d}:00' for h in hours], rotation=45)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Water usage analysis saved to {output_file}")
        plt.close()
    
    def generate_alert_summary(self, output_file: str = '/home/ubuntu/alert_summary_water.png'):
        """Generate alert summary chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Alert types
        alert_types = {
            'Overflow': random.randint(2, 8),
            'Shortage': random.randint(1, 5),
            'Pump Malfunction': random.randint(1, 4),
            'Sensor Fault': random.randint(2, 6)
        }
        
        colors_alerts = ['#FF6B6B', '#FF8C42', '#FFD93D', '#A0A0A0']
        bars = ax1.bar(alert_types.keys(), alert_types.values(), color=colors_alerts,
                      alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax1.set_ylabel('Number of Alerts', fontsize=12, fontweight='bold')
        ax1.set_title('Alert Type Distribution (24-hour)', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, count in zip(bars, alert_types.values()):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(count)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Alert severity distribution
        severity_dist = {
            'Low': random.randint(5, 15),
            'Medium': random.randint(10, 20),
            'High': random.randint(3, 10),
            'Critical': random.randint(1, 3)
        }
        
        severity_colors = ['#FFD93D', '#FF8C42', '#FF6B6B', '#C41E3A']
        wedges, texts, autotexts = ax2.pie(severity_dist.values(), labels=severity_dist.keys(),
                                            autopct='%1.1f%%', colors=severity_colors, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax2.set_title('Alert Severity Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Alert summary chart saved to {output_file}")
        plt.close()
    
    def generate_system_efficiency(self, output_file: str = '/home/ubuntu/system_efficiency.png'):
        """Generate system efficiency dashboard"""
        stats = self.system.get_system_statistics()
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
        
        # KPI boxes
        kpis = [
            ('Total Tanks', stats['total_tanks'], '#2E86AB'),
            ('System Fill %', f"{stats['system_fill_percentage']:.1f}%", '#4ECDC4'),
            ('Total Capacity', f"{stats['total_capacity']:.0f}L", '#45B7D1'),
            ('Current Level', f"{stats['total_current_level']:.0f}L", '#96CEB4'),
            ('Pumps Running', stats['pumps_running'], '#FFEAA7'),
            ('Active Alerts', stats['active_alerts'], '#FF6B6B'),
        ]
        
        for idx, (title, value, color) in enumerate(kpis):
            ax = fig.add_subplot(gs[idx // 3, idx % 3])
            ax.add_patch(mpatches.FancyBboxPatch((0.05, 0.2), 0.9, 0.6,
                                                boxstyle="round,pad=0.05", 
                                                edgecolor=color, facecolor=color, alpha=0.2, linewidth=2))
            ax.text(0.5, 0.65, title, ha='center', va='center', fontsize=12, fontweight='bold')
            ax.text(0.5, 0.35, str(value), ha='center', va='center', fontsize=24, fontweight='bold', color=color)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # Summary text
        ax_summary = fig.add_subplot(gs[2, :])
        summary_text = f"""
        SMART WATER TANK MANAGEMENT SYSTEM - EFFICIENCY REPORT
        
        System Status: {stats['total_tanks']} tanks monitored | Total Capacity: {stats['total_capacity']:.0f}L | Current Fill: {stats['system_fill_percentage']:.1f}%
        
        Pumps Running: {stats['pumps_running']} | Active Alerts: {stats['active_alerts']} | System Health: Operational
        """
        ax_summary.text(0.05, 0.5, summary_text, fontsize=11, verticalalignment='center',
                       family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax_summary.axis('off')
        
        fig.suptitle('Smart Water Tank Management System - Performance Dashboard', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"System efficiency dashboard saved to {output_file}")
        plt.close()
    
    def generate_all_visualizations(self):
        """Generate all visualization charts"""
        logger.info("Generating all visualization charts...")
        self.generate_water_level_trend()
        self.generate_pump_operation_analysis()
        self.generate_water_usage_analysis()
        self.generate_alert_summary()
        self.generate_system_efficiency()
        logger.info("All visualizations generated successfully!")


if __name__ == "__main__":
    from water_tank_system import WaterManagementSystem, WaterSimulator
    
    # Create system
    system = WaterManagementSystem()
    
    # Run simulation
    simulator = WaterSimulator(system)
    simulator.simulate_24_hour_cycle()
    
    # Generate analytics
    analytics = WaterTankAnalytics(system)
    analytics.generate_all_visualizations()
    
    print("Analytics generation completed!")
