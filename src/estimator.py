#estimate currently infected
def estimate_currently_infected(reported_cases):
  impact = reported_cases * 10
  severe_impact = reported_cases * 50
  return {"impact": impact, "severe_impact":severe_impact}

#estimate infections by requestedTime
def infections_by_requested_time(current, period_type, count):
  if period_type == "months":
    days = count * 30
  elif period_type == "weeks":
    days = count * 7
  elif period_type == "days": 
    days = count 
  else:
    raise ValueError("Unrecognised periodType")
  impact = current["impact"] * 2**(days//3)
  severe_impact = current["severe_impact"] * 2**(days//3)
  return {"impact": impact, "severe_impact":severe_impact}

#approximate number of severe cases with given time
def get_severe_cases_with_time(infections):
  return {"impact": int(infections["impact"]*0.15), "severe_impact": int(infections["severe_impact"]*0.15)}

#estimate number of beds available
def estimate_available_beds(severe_cases, total_hospital_beds):
  available_beds = total_hospital_beds * 0.35
  if severe_cases["impact"] <= available_beds:
    impact = int(available_beds)
  else:
    impact = int(-(severe_cases["impact"] - available_beds))
    
  if severe_cases["severe_impact"] <= available_beds:
    severe_impact = int(available_beds)
  else:
    severe_impact = int(-(severe_cases["severe_impact"] - available_beds))
  
  return {"impact":impact, "severe_impact":severe_impact}

# calculate casesForICUByRequestedTime
def estimate_icu_cases_with_time(infections_with_time):
  return {
    "impact": int(infections_with_time["impact"] * 0.05),
    "severe_impact": int(infections_with_time["severe_impact"] * 0.05)
  }

# calculate casesForVentilatorsByRequestedTime
def estimate_ventilator_cases_with_time(infections_with_time):
  return {
    "impact": int(infections_with_time["impact"] * 0.02),
    "severe_impact": int(infections_with_time["severe_impact"] * 0.02)
  }

# compute dollarsInFlight 
def compute_dollars_in_flight(infections_with_time, pop_pct,avg_income, period, count):
  if period == "months":
    days = count * 30
  elif period == "weeks":
    days = count * 7
  elif period == "days": 
    days = count 
  else:
    raise ValueError("Unrecognised periodType")
  
  impact_usd = infections_with_time["impact"] * pop_pct * avg_income * days
  severe_impact_usd =  infections_with_time["severe_impact"] * pop_pct * avg_income * days
  return {"impact": round(impact_usd, 2), "severe_impact": round(severe_impact_usd, 2)}

def estimator(data):
  #set CurrentlyInfected
  currently_infected = estimate_currently_infected(data["reportedCases"])
  
  #set InfectionsByRequestedTime
  predicted_infections_by_time = infections_by_requested_time(currently_infected, data["periodType"], data["timeToElapse"])
  
  #severeCasesByRequestedTime
  severe_cases = get_severe_cases_with_time(predicted_infections_by_time)
  
  #hospitalBedsByRequestedTime
  hospital_beds = estimate_available_beds(severe_cases, data["totalHospitalBeds"])
  
  #casesForICUByRequestedTime
  icu_cases = estimate_icu_cases_with_time(predicted_infections_by_time)
  
  #casesForVentilatorsByRequestedTime
  ventilator_cases =  estimate_ventilator_cases_with_time(predicted_infections_by_time)
  
  #dollarsInFlight
  avg_pop = data["region"]["avgDailyIncomePopulation"]
  avg_usd = data["region"]["avgDailyIncomeInUSD"]
  period = data["periodType"]
  count = data["timeToElapse"]
  dollars_in_flight = compute_dollars_in_flight(predicted_infections_by_time, avg_pop, avg_usd, period, count)
  
  
  impact_estimation={ 
    "data": data, 
    "impact": {
      "currentlyInfected": currently_infected["impact"],
      "infectionsByRequestedTime":predicted_infections_by_time["impact"],
      "severeCasesByRequestedTime": severe_cases["impact"],
      "hospitalBedsByRequestedTime": hospital_beds["impact"],
      "casesForICUByRequestedTime": icu_cases["impact"],
      "casesForVentilatorsByRequestedTime": ventilator_cases["impact"],
      "dollarsInFlight": dollars_in_flight["impact"]
      }, 
    "severeImpact":{
      "currentlyInfected": currently_infected["severe_impact"],
      "infectionsByRequestedTime": predicted_infections_by_time["severe_impact"],
      "severeCasesByRequestedTime": severe_cases["severe_impact"],
      "hospitalBedsByRequestedTime": hospital_beds["severe_impact"],
      "casesForICUByRequestedTime": icu_cases["severe_impact"],
      "casesForVentilatorsByRequestedTime": ventilator_cases["severe_impact"],
      "dollarsInFlight": dollars_in_flight["severe_impact"]
      } 
    }
  
  return impact_estimation

