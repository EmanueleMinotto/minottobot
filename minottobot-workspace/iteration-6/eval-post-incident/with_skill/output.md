Norsk Mobility AS, thank you for sharing this information with me. I'm glad we could have this conversation.

Based on what you've shared, here's a summary of our findings so far:

**Key Findings:**

1. **Evolving E2E testing landscape**: With the recent addition of 12 new E2E tests written in the last week, it's clear that your team is taking E2E testing seriously. However, I'd like to explore more about the process behind these new tests and how they fit into your overall testing strategy.
2. **Manual approval gate for CI**: The ~12-minute GitHub Actions workflow with a manual approval gate before production deployment suggests that there's an opportunity to improve the efficiency of this process. Have you considered automating some or all of these steps?
3. **Deployment frequency and incident**: While your deployment frequency is relatively low (1-2 times per week), the recent incident involving a race condition in your payment processing service is a concerning sign. I'd like to discuss ways to improve your monitoring setup and ensure that similar incidents are caught earlier.
4. **Lack of test coverage for critical areas**: With only 340 unit tests, 45 integration tests, and 12 E2E tests, it's clear that there's still room for growth in terms of test coverage. I'd like to explore ways to increase the overall testing coverage, particularly for critical areas such as payment processing.

**Recommendations:**

1. **Improve E2E testing process**: Let's discuss how you can refine your E2E testing process to ensure that it's scalable and maintainable.
2. **Automate manual approval gate**: Consider automating the manual approval gate for CI workflows to reduce the time spent on this step and improve overall efficiency.
3. **Enhance monitoring setup**: Given the recent incident, I recommend exploring ways to improve your Sentry setup, such as adding more monitors or integrating with other tools to catch issues earlier.
4. **Increase test coverage**: Let's discuss strategies for increasing test coverage across critical areas of the application.

**Next Steps:**

1. **Conduct a code review**: I'd like to conduct a high-level review of your codebase to identify potential areas for improvement and provide recommendations for refactoring or optimizing certain components.
2. **Gather feedback from engineers**: Can you gather feedback from your engineering team about their pain points, challenges, and suggestions for improving the testing process?

How do these findings and recommendations align with your goals and priorities? Are there any questions or concerns you'd like to discuss further?
