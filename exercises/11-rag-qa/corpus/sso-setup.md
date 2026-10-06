---
title: Single sign-on (SSO) and SCIM
last_updated: 2026-01-22
---
# Single sign-on (SSO) and SCIM

SSO and SCIM are available on the **Business** plan only.

## Supported identity providers
Tidepool supports SAML 2.0 SSO with Okta, Microsoft Entra ID (formerly Azure AD), and Google Workspace. Other SAML 2.0 providers usually work but aren't officially supported.

## Setting up SSO
1. In Tidepool, go to **Settings > Security > SSO** and copy the ACS URL and Entity ID.
2. Create a SAML app in your identity provider using those values.
3. Paste the identity provider's metadata URL back into Tidepool.
4. Test with one account before you enable **Require SSO** for everyone.

## SCIM provisioning
SCIM lets your identity provider create, update, and deactivate Tidepool users automatically. Generate a SCIM token under **Settings > Security > SCIM**. Tokens don't expire, but you can revoke them at any time.
