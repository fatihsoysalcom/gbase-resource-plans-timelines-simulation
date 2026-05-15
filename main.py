import datetime
import random

# 1. Define Workload Types
# Each workload has a base cost representing its resource consumption (e.g., CPU, I/O units).
class Workload:
    def __init__(self, name, base_cost):
        self.name = name
        self.base_cost = base_cost # Represents generic resource units needed

    def __repr__(self):
        return f"Workload('{self.name}', cost={self.base_cost})"

# Predefined workload types for the simulation
OLTP_QUERY = Workload("OLTP_Query", 10)       # Online Transaction Processing: typically small, fast queries
REPORTING_QUERY = Workload("Reporting_Query", 50) # Analytical queries: moderate resource consumption
BATCH_JOB = Workload("Batch_Job", 200)      # Long-running jobs: high resource consumption

# 2. Define Resource Plans
# Each plan dictates how much 'priority' or 'resource share' each workload type receives.
# A higher 'priority_factor' means the workload effectively consumes fewer resource units
# per unit of work, thus completing faster or taking less of the total resource pool.
RESOURCE_PLANS = {
    "BUSINESS_HOURS_PLAN": {
        OLTP_QUERY.name: 1.5,      # High priority during business hours
        REPORTING_QUERY.name: 1.0, # Normal priority
        BATCH_JOB.name: 0.2,       # Low priority, to not impact OLTP/Reporting
    },
    "NIGHTLY_BATCH_PLAN": {
        OLTP_QUERY.name: 0.5,      # Lower priority at night
        REPORTING_QUERY.name: 0.8, # Slightly lower
        BATCH_JOB.name: 2.0,       # High priority for batch jobs during off-peak hours
    },
    "WEEKEND_PLAN": {
        OLTP_QUERY.name: 1.0,
        REPORTING_QUERY.name: 1.5, # More reporting/analysis might happen on weekends
        BATCH_JOB.name: 1.0,
    }
}

# 3. Define Timelines
# A timeline specifies which resource plan is active during certain periods.
# Format: (start_hour, end_hour, list_of_days_of_week, plan_name)
# day_of_week: 0=Monday, 6=Sunday.
# Note: If end_hour < start_hour, the plan spans across midnight (e.g., 17 to 9).
TIMELINE = [
    # Business hours (Monday-Friday, 9 AM - 5 PM)
    (9, 17, [0, 1, 2, 3, 4], "BUSINESS_HOURS_PLAN"),
    # Nightly batch (Monday-Friday, 5 PM - 9 AM next day)
    (17, 9, [0, 1, 2, 3, 4], "NIGHTLY_BATCH_PLAN"),
    # Weekend (Saturday & Sunday, all day)
    (0, 24, [5, 6], "WEEKEND_PLAN"),
]

# Helper function to determine the active plan for a given time
def get_active_plan(current_datetime):
    current_hour = current_datetime.hour
    current_day = current_datetime.weekday() # 0=Monday, 6=Sunday

    for start_h, end_h, days, plan_name in TIMELINE:
        if current_day not in days: # Check if the current day matches the plan's days
            continue

        if start_h < end_h: # Plan active within the same day (e.g., 9 AM to 5 PM)
            if start_h <= current_hour < end_h:
                return RESOURCE_PLANS[plan_name]
        else: # Plan spans across midnight (e.g., 5 PM to 9 AM)
            if current_hour >= start_h or current_hour < end_h:
                return RESOURCE_PLANS[plan_name]
    return None # No specific plan found, might imply a default or no-op

# 4. Simulate Workload Processing
def simulate_workload_processing(current_datetime, workloads_to_process, available_resource_units_per_hour):
    active_plan = get_active_plan(current_datetime)
    if not active_plan:
        print(f"[{current_datetime.strftime('%Y-%m-%d %H:00')}] No active plan found. Workloads might be stalled.")
        return

    print(f"\n--- {current_datetime.strftime('%Y-%m-%d %H:00')} ---")
    # Find the name of the active plan for display
    active_plan_name = next((name for name, plan in RESOURCE_PLANS.items() if plan == active_plan), "Unknown Plan")
    print(f"Active Plan: {active_plan_name}")

    processed_workloads = []
    remaining_resource_units = available_resource_units_per_hour

    # Calculate effective costs based on the active plan's priority factors
    workloads_with_effective_cost = []
    for workload in workloads_to_process:
        # Get priority factor from the active plan; default to 1.0 if not specified
        priority_factor = active_plan.get(workload.name, 1.0)
        # Effective cost is base cost divided by priority factor. Higher factor -> lower effective cost -> higher priority.
        effective_cost = workload.base_cost / priority_factor
        workloads_with_effective_cost.append((workload, effective_cost))

    # Sort workloads by their effective cost (lower effective cost means higher priority/faster processing)
    workloads_with_effective_cost.sort(key=lambda x: x[1])

    print(f"Workloads to process (sorted by effective priority):")
    for workload, effective_cost in workloads_with_effective_cost:
        priority_factor = active_plan.get(workload.name, 1.0)
        print(f"  - {workload.name} (Base Cost: {workload.base_cost}, Priority Factor: {priority_factor:.1f}, Effective Cost: {effective_cost:.1f})")

    # Simulate processing by allocating available resource units
    for workload, effective_cost in workloads_with_effective_cost:
        if remaining_resource_units >= effective_cost:
            remaining_resource_units -= effective_cost
            processed_workloads.append(workload)
            print(f"  Processed {workload.name} (Effective Cost: {effective_cost:.1f}). Remaining resources: {remaining_resource_units:.1f}")
        else:
            print(f"  Could not fully process {workload.name} (Effective Cost: {effective_cost:.1f}) due to insufficient resources. Remaining: {remaining_resource_units:.1f}")
            # In a real system, this might mean partial processing, queuing, or slower execution.
            break # Stop if resources are depleted for this hour

    print(f"Total processed: {len(processed_workloads)} workloads.")
    return processed_workloads

# --- Main Simulation Loop ---
if __name__ == "__main__":
    print("GBase 8a Resource Plan and Timeline Integration Simulation\n")

    start_date = datetime.datetime(2023, 10, 26, 8, 0, 0) # Start simulation on a Thursday at 8 AM
    simulation_duration_hours = 48 # Simulate 2 full days

    available_resource_units_per_hour = 300 # A fixed pool of resources available each simulated hour

    for i in range(simulation_duration_hours):
        current_time = start_date + datetime.timedelta(hours=i)

        # Generate some random workloads for the current hour to demonstrate varying demands
        current_workloads = []
        if current_time.weekday() in [0, 1, 2, 3, 4]: # Weekday workload generation
            if 9 <= current_time.hour < 17: # Business hours (9 AM - 5 PM)
                current_workloads.extend([OLTP_QUERY] * random.randint(5, 10))
                current_workloads.extend([REPORTING_QUERY] * random.randint(1, 3))
                current_workloads.extend([BATCH_JOB] * random.randint(0, 1))
            else: # Night/Off-hours (5 PM - 9 AM)
                current_workloads.extend([OLTP_QUERY] * random.randint(1, 3))
                current_workloads.extend([REPORTING_QUERY] * random.randint(0, 1))
                current_workloads.extend([BATCH_JOB] * random.randint(2, 5))
        else: # Weekend workload generation
            current_workloads.extend([OLTP_QUERY] * random.randint(2, 5))
            current_workloads.extend([REPORTING_QUERY] * random.randint(2, 4))
            current_workloads.extend([BATCH_JOB] * random.randint(1, 2))

        simulate_workload_processing(current_time, current_workloads, available_resource_units_per_hour)
