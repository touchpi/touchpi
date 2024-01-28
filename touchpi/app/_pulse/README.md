## pulse core app
This is a background app. It counts in second and sends pulse event which can be used by other apps. 
The basic pulse time unit is in second and the multiples of it can be configured.
This core app is optional and can be disabled in the core settings. 

Samples: 
- pulse_in_second = **1** and pulse_factors = [1, 60, 3600] will send events '-pulse 1-', '-pulse 60-' and '-pulse 3600-'
- pulse_in_second = **5** and pulse_factors = [1, 3, 12, 120, 360, 720] will send events '-pulse 5-', '-pulse 15-', '-pulse 60-', '-pulse 600-', '-pulse 1800-' and '-pulse 3600-'
- pulse_in_second = **0.25** and pulse_factors = [1, 4, 40] will send events '-pulse 0.25-', '-pulse 1- and '-pulse 10-'
