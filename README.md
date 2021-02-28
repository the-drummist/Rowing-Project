# Rowing Capstone  

## Integrated Software  
None of the software has been tested yet. It will only run on a raspberry pi.  
The software for testing is outlined in data_collection.py and devices.py  
Parts of devices.py and all of hrcalc.py are modified from a 3rd party library due to time constraints.  

## Website  

### Routes 

| User Route            | Description                                   | Method   | Authenticated |
| --------------------- | --------------------------------------------- | -------- | ------------- |
| /dashboard/\<username>| Home page, has graph’s and other main features| GET      | True          |
| /account/settings     | Update account settings and personal details  | GET/POST | True          |
| /register             | Register an account                           | GET/POST | False         |
| /login                | Log in to account/create session              | GET/POST | False         |
| /logout               | Log out of account and clear session          | GET      | True          |
| /account/upload       | User Post's the workout data                  | GET/POST | True          |
| /upload/\<username>   | Only if time: When the device connects to WiFi, automatically upload workout data. Each account needs a unique UUID that will be uploaded with the data to verify the device is associated with the account | POST     | False         |  

| Info Route (CIJE) | Description |
| ----------------- | ----------- |
| TODO              | TODO        |  

### User Dashboard  

| Component                     | Description | 
| ----------------------------- | ----------- |
| EMG Graph                     | A line graph of the EMG reading for the most recent workout. the graphs background is green in the safe range and red in the dangerous range |
| Pulse Graph                   | A line graph of the Pulse reading for the most recent workout. [Calculate](http://diet.mayoclinic.org/diet/move/how-to-measure-exercise-intensity?xid=nl_MayoClinicDiet_20160523) based on age the ideal zone for someone during a workout. The ideal zone is green, and anything above and below it is red. |
| SpO2 Graph                    | A line graph of the SpO2 reading for the most recent workout.  The ideal zone is green (88% to 92%), anything below it is red and anything above it is yellow. |
| Calculated Shear Loding Graph | A line graph calculated by smoothing out the EMG reading and mapping it to corresponding force values (experimental) |
| Calculated Intensity Graph    | A line graph calculated by the equation ```MET's = (15.3 * (MHR/RHR)) / 3.5``` (Alex Kramer spent forever finding information and deriving this equation (:  |
| Calories Burned Calculation   | The Number of Calories Burned during the Workout. [Calculated](https://burned-calories.com/heart-rate) based on age, weight, and heart rate | 
| Calculated Progress Graph     | A line graph containing the average of each component from each workout plotted |