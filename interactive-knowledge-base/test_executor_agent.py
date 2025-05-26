from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

MODEL = "gpt-4o"
TEMPERATURE = 0

"""
Agent for executing test plan.
This agent uses browser_use to automate browser interactions.
"""

llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

async def execute():
    task = """
## Your Task
Go to http://localhost:3000/
Execute an end-to-end test plan below for testing the declining flow of the Quick Loan Platform.
Return the results in markdown format. Action, Expected Result and Actual Result for each step.

### Test Plan: Declining Flow

#### Step 1: User Accesses Loan Application Form
- **Action**: Navigate to the Quick Loan Platform and start a new loan application.
- **Expected Result**: The loan application form loads successfully.

#### Step 2: User Submits Loan Application with Decline Criteria
- **Action**: Fill out the application form with details that meet the decline criteria (e.g., annual revenue less than $50,000, business operation less than two years).
Entered values can not be 0. EIN is required.
Complete "Personal Information", "Business Information", "Loan Details" sections first.
Scroll down on "Review & Submit" to hit the "Submit Application" button.
- **Expected Result**: The form validates the input and allows submission.

#### Step 3: Backend Processes Application and Declines
- **Action**: Submit the application.
- **Expected Result**: The backend processes the application, identifies it meets the decline criteria, and sets the application status to 'DECLINED'. This status is saved in the database.

#### Step 4: Frontend Displays Decline Decision
- **Action**: Wait for the response from the backend.
- **Expected Result**: The frontend receives the declined status and displays a message with a red "XCircle" icon stating, "Unfortunately, your loan application has been declined. Please contact our support team for more information."

#### Step 5: User Receives Decline Notification
- **Action**: Review the displayed message and icon.
- **Expected Result**: The message and icon are clearly visible and correctly convey the declined status of the application.
    """

    agent = Agent(
        task=task,
        llm=llm,
    )
    result = await agent.run()
    print("-" * 100)
    print(result)

if __name__ == "__main__":
    asyncio.run(execute())
