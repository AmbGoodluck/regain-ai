# Regain Ai

## Build Plan
# Build Plan: Regain AI: Lean MVP

**Solo founder, Expo/React + Supabase + Cloudflare + TypeScript**  
**Target ship: 8–12 weeks**

---

## Core MVP Features (P0 only)

1. **Lead intake + ledger**: Web form webhook, missed-call detection, single source-of-truth Postgres table with status lifecycle (new → calling → booked/no_answer/not_interested).

2. **AI callback engine**: Outbound call placed within 60s using cloned voice (ElevenLabs), injected lead context, hardcoded qualification questions, Cal.com booking.

3. **Live transcript + human takeover**: Streaming transcript UI during call, one-click handoff to owner's phone, post-call summary + full transcript saved.

4. **Leads ledger UI**: Filterable list (All/Live/Booked/Recovered), detail view per lead, note-taking, status timeline.

5. **Onboarding wizard + compliance**: 5-step setup (profile → lead sources → calendar → voice consent + clone → go live), consent record per voice, no callable lead without consent basis.

**What's excluded (P1+):** revenue dashboard, AI training UI, multi-voice roster, follow-ups, SMS, CRM sync, native apps, multi-location.

---

## Stack

| Layer | Tech | Why |
|-------|------|-----|
| **Frontend** | Expo (React Native) web build | One codebase, ship a link, no app-store friction. Mobile later. |
| **Auth + DB** | Supabase (Postgres) | Real-time subscriptions for live transcript, built-in RLS for multi-tenant ledger, edge functions for webhooks. |
| **Edge + Workers** | Cloudflare Workers | Lead-arrival webhook → 60s call trigger, fallback handling, low latency, free tier sufficient for MVP. |
| **Voice infra** | Vapi or Retell (rented) | Handles PSTN, TTS, STT; Regain layers reliability + transcript. |
| **Voice cloning** | ElevenLabs | Consent-gated, simple API, quality. |
| **Calendar** | Cal.com API | Free tier, multi-provider (Google/Outlook), no custom sync needed. |
| **Deployment** | Vercel (web), Supabase (DB + functions) | Expo web → Vercel, zero config. Functions live in Supabase. |

---

## 4-Step Milestones

### **Milestone 1: Foundation (Weeks 1–3)**
**Goal:** Supabase ledger + web auth + onboarding wizard MVP  
- [ ] Supabase schema: `businesses`, `users`, `leads`, `voices` (consent, not clone yet).
- [ ] Expo web build scaffold + Supabase auth (magic link).
- [ ] Onboarding wizard (step 1-4): biz profile form, Cal.com OAuth, voice consent record (no cloning yet, just store the rep's name/phone).
- [ ] Leads table schema with `consent_basis` field; add leads via POST webhook (unsigned for now; add signature verification in P1).
- [ ] Basic leads list UI (all/status filter, detail view, note field).
- [ ] Deploy Expo web to Vercel.  
**Ship a link:** founder can sign up, add a business, see an empty ledger, and prepare for incoming leads.

### **Milestone 2: Lead capture + voice (Weeks 4–6)**
**Goal:** Webhook intake, voice cloning, 60s call trigger  
- [ ] Cloudflare Worker listening on `POST /api/lead` for form submissions and missed-call webhooks.
- [
