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

def estimator(data):
  #set CurrentlyInfected
  currently_infected = estimate_currently_infected(data["reportedCases"])
  
  #set InfectionsByRequestedTime
  predicted_infections_by_time = infections_by_requested_time(currently_infected, data["periodType"], data["timeToElapse"])
  
  impact_estimation={ 
    "data": data, 
    "impact": {
      "currentlyInfected": currently_infected["impact"],
      "infectionsByRequestedTime":predicted_infections_by_time["impact"]
      }, 
    "severeImpact":{
      "currentlyInfected": currently_infected["severe_impact"],
      "infectionsByRequestedTime": predicted_infections_by_time["severe_impact"]
      } 
    }
  return impact_estimation

