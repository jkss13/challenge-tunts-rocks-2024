import os.path
import functions as func

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "11w76n5v3_g1N8lO-ipXNYVH1CaxF7Th_tdTu5BOo8w0"
SAMPLE_RANGE_NAME = "engenharia_de_software!A3:H27"

def main():
	"""Shows basic usage of the Sheets API.
	Prints values from a sample spreadsheet.
	"""
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
			"credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open("token.json", "w") as token:
			token.write(creds.to_json())

	try:
		service = build("sheets", "v4", credentials=creds)

		# Call the Sheets API 
		result = (
			service.spreadsheets()
			.values()
			.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
			.execute()
		)

		values = result.get("values", [])
	
		student_situation = [
			["Situação"],
		]

		final_grade_to_be_approved = [
			["Nota para Aprovação Final"],
		]

		data = [
        {"range": "G3", "values": student_situation},
		{"range": "H3", "values": final_grade_to_be_approved},
		]

		body = {"valueInputOption": "USER_ENTERED", "data": data}

		for i, row in enumerate(values):
			if i > 0:
				absences = int(row[2])
				p1 = int(row[3])
				p2 = int(row[4])
				p3 = int(row[5])
				grades_average = (p1 + p2 + p3) / 3
				status = func.calculate_status(grades_average, absences)
				final_passing_grade = func.calculate_final_passing_grade(grades_average, status)

				student_situation.append([status])
				final_grade_to_be_approved.append([final_passing_grade])

		result = (
			service.spreadsheets()
			.values()
			.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
			body=body)
			.execute()
		)

		print("Congrats! Your spreadsheet has been updated successfully!")

	except HttpError as err:
		print(err)

if __name__ == "__main__":
	main()