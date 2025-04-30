# Bug Report: No Feedback After Invalid Login Attempt

## Title
No feedback after invalid login attempt

## Environment
- URL: [https://bookcart.azurewebsites.net/](https://bookcart.azurewebsites.net/)
- Browser: Chrome (latest)
- OS: macOS / Linux (tested on both)

## Priority
Medium

## Steps to Reproduce
1. Open the homepage.
2. Click on the "Login" button.
3. Enter an invalid username and password.
4. Press Enter or click the "Login" button.

## Expected Result
An error message like **"Invalid username or password"** should appear, informing the user that the login failed.

## Actual Result
No error message is displayed.  
The page remains unchanged, giving no feedback to the user.

## Notes
- This can confuse users and make them think the site is unresponsive.
- Proper user feedback should be added for invalid login attempts.

## Status
Open
