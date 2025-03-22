It seems like you're referring to the naming conventions used in the endpoints. Here's a breakdown of how the endpoints adhere to common naming conventions:

### **Naming Conventions**
1. **Use of Plural Nouns**: Endpoints like `/users`, `/admin/dashboards`, and `/tokens` use plural nouns, which is consistent with RESTful API best practices for collections.

2. **Use of Nouns Instead of Verbs**: Endpoints are named using nouns (e.g., `/users`, `/tokens`) rather than verbs (e.g., `createUser`, `clearTokens`). This is correct, as HTTP methods (POST, GET, PUT, DELETE) already convey the action.

3. **Consistent Use of Slashes**: The endpoints consistently use slashes (`/`) to separate different parts of the path, which helps in nesting related resources.

4. **Lowercase Letters and Hyphens**: The endpoints use lowercase letters and do not include hyphens except in cases like `/admin-dashboards`, which is not present here but would be a good practice for readability.

### **Improvement Suggestions**
- **Consistency in Singular vs. Plural**: Ensure that all collection endpoints use plural nouns (e.g., `/admin/dashboards` instead of `/admin/dashboard`).
- **Avoid Special Characters**: While not present here, it's generally advisable to avoid special characters unless they significantly improve readability.

### **Example of Improved Consistency**
- **Before**: `/admin/dashboard`
- **After**: `/admin/dashboards`

By following these conventions, the endpoints are more intuitive and easier to understand for developers using your API.

### **Table with Endpoints**
Here's the table again for reference:

| **Endpoint**                  | **HTTP Method** | **Protected** | **Description**                                  |
|-------------------------------|-----------------|---------------|--------------------------------------------------|
| `/token`                      | `POST`          | No            | Authenticates user and returns access/refresh tokens |
| `/refresh-token`              | `POST`          | Yes (Refresh Token) | Issues a new access token using refresh token       |
| `/signup`                     | `POST`          | No            | Registers new users with USER role                |
| `/users`                      | `POST`          | Yes (ADMIN)   | Creates users with any role                        |
| `/users/me`                   | `GET`           | Yes (USER)    | Returns current user's details                     |
| `/users/me/items`             | `GET`           | Yes (USER)    | Returns items belonging to current user            |
| `/admin/dashboards`           | `GET`           | Yes (ADMIN)   | Returns admin dashboard with user statistics        |
| `/tokens/clear`               | `POST`          | No            | Clears all tokens in the system                   |

This table reflects the improved naming conventions and consistency across the endpoints.

---
Answer from Perplexity: pplx.ai/share