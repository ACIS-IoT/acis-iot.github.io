# Estimation of Mean Time Between Attacks and Rate

This project aims to estimate the mean time between attacks and the attack rate using different methods. The provided command should be executed to obtain the results.

## Execution Command

To execute the command, run the following command in your terminal:

```bash
python3 main.py ARP data.csv 6 84
```

This command takes the following parameters:
- `ARP`: Attack type
- `data.csv`: CSV file containing the attack data
- `6`: Column index of the time column in the CSV file
- `84`: Column index of the attack column in the CSV file

## Results

After executing the command, the program will output the following results:

- **Attack:** ARP
- **CSV File:** data.csv
- **Time Column:** 6
- **Attack Column:** 84

The estimated mean time between attacks is 7.414857530529172 seconds.

The estimated rate parameter using the classical method is 0.13486435793037194.

The estimated rate parameter using Maximum Likelihood Estimation (MLE) with the solver L-BFGS-B is 0.13486435351259937.

The estimated rate parameter using MLE with the Nelder-Mead solver is 0.13486328124999925.

Feel free to modify the command or explore the code further to suit your needs. If you have any questions or need assistance, please let me know!

