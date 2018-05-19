import pygsheets

gc = pygsheets.authorize(outh_file='./client_secret.json', outh_nonlocal=True)
sh = gc.open("Copy of New Owner Onboarding")

all_new_owners_sheet = sh.worksheet_by_title("All New Owners")
new_owner_onboarding_tracking_sheet = sh.worksheet_by_title("New Owner Onboarding Tracking")

for row in all_new_owners_sheet:
    print(row)

for row in new_owner_onboarding_tracking_sheet:
	print(row)