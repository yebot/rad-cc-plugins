# Example: Code Review

This is a sample output from `/code-review src/components/LoginForm.tsx`.

---

## Code Review Summary

**Files Reviewed**: 1
**Overall Assessment**: Needs Work

---

### Critical Issues (Must Fix)

| Issue | Location | Severity |
|-------|----------|----------|
| Password sent to analytics | `LoginForm.tsx:45` | Critical |
| No rate limiting mentioned | `LoginForm.tsx:38` | Critical |

### Suggestions (Should Fix)

| Suggestion | Location | Impact |
|------------|----------|--------|
| Add input sanitization | `LoginForm.tsx:32` | High |
| Missing loading state for submit button | `LoginForm.tsx:52` | Medium |
| Form doesn't handle network errors | `LoginForm.tsx:40-48` | Medium |
| Missing aria-describedby for errors | `LoginForm.tsx:28` | Medium |

### Minor Comments (Nice to Have)

- Consider using `useId()` for form field IDs at `LoginForm.tsx:15`
- Password field could use `autoComplete="current-password"` at `LoginForm.tsx:25`
- Form could benefit from optimistic UI feedback

---

### Full-Stack Engineer Notes

**Overall**: The form logic is solid but missing important edge cases and error handling.

**Recommendations**:
1. Add proper error boundary for unexpected errors
2. Implement retry logic for failed submissions
3. Consider form state library (react-hook-form) for complex validation
4. Add unit tests for validation logic

**Code Quality**:
- Types are well-defined
- Component is appropriately sized
- Good separation of concerns

---

### Security Engineer Notes

**Critical Security Issues**:

1. **Password Logging** (Line 45)
   ```typescript
   // REMOVE THIS - Never log credentials
   analytics.track('login_attempt', { email, password });
   ```
   This sends the user's password to your analytics service. This is a severe security vulnerability.

2. **Missing CSRF Protection**
   No CSRF token visible in the form submission. Ensure your API validates CSRF tokens.

3. **Rate Limiting**
   No client-side rate limiting. Add:
   - Disable button after failed attempts
   - Show lockout message after N failures
   - Work with backend team on server-side rate limiting

**Security Checklist**:
- [ ] Remove password from analytics
- [ ] Add CSRF token
- [ ] Implement rate limiting
- [ ] Add failed attempt tracking
- [ ] Consider adding CAPTCHA after failed attempts

---

### QA Engineer Notes

**Recommended Tests**:

**Unit Tests**:
- [ ] Email validation (valid, invalid, edge cases)
- [ ] Password validation (empty, too short, valid)
- [ ] Form submission with valid data
- [ ] Form submission with invalid data

**Integration Tests**:
- [ ] Successful login redirects correctly
- [ ] Failed login shows error message
- [ ] Loading state displays during submission
- [ ] Form clears password on failed attempt

**E2E Tests**:
- [ ] Complete login flow (happy path)
- [ ] Login with invalid credentials
- [ ] Login with account lockout
- [ ] Remember me functionality (if applicable)

**Edge Cases to Test**:
- Network timeout during submission
- Concurrent form submissions
- Browser autofill behavior
- Password manager integration

---

### Frontend Engineer Notes

**Component Structure**: Good

**Accessibility Issues**:
1. Error messages need `aria-describedby` connection to inputs
2. Add `aria-invalid` when fields have errors
3. Focus should move to first error on failed submission

**Suggested Improvements**:
```typescript
// Add to password input
<input
  type="password"
  aria-invalid={!!errors.password}
  aria-describedby={errors.password ? "password-error" : undefined}
  autoComplete="current-password"
/>

// Error message
{errors.password && (
  <span id="password-error" role="alert">
    {errors.password}
  </span>
)}
```

**Performance**: No concerns - form is lightweight

---

### Approval Status

- [ ] Full-Stack: Changes Requested
- [ ] Security: **Changes Requested (Blocking)**
- [ ] QA: Changes Requested (Non-blocking)
- [ ] Frontend: Changes Requested (Non-blocking)

**Summary**: Cannot merge until security issues are resolved. Password logging is a critical vulnerability that must be fixed immediately.
