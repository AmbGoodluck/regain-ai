# Product Requirements Document — Regain AI

**Version:** 1.0
**Owner:** Osman
**Status:** Draft for build
**Last updated:** June 2026

---

## 1. One-line summary

Regain AI is an AI-powered lead recovery system that calls a service business's missed calls and web-form leads back within 60 seconds in their own rep's voice, books the appointment, and tracks the revenue recovered, so contractors stop losing jobs to whoever picks up the phone first.

## 2. Problem

Service businesses lose a large share of paid-for leads to slow follow-up. Industry data is unambiguous: responding within 5 minutes makes a business up to 100x more likely to reach the lead and the first responder wins ~78% of deals, yet only ~0.1% of field-service businesses respond within 5 minutes and the average response time is 42 to 47 hours. Around 40% of leads arrive after hours or on weekends, when nobody is available. The result is that contractors pay for leads through ads and referrals, then lose 60 to 75% of that spend to delay. They cannot fix it by "telling staff to be faster," because the gap is structural: owners are on rooftops, offices are closed at night, and humans cannot answer instantly every time.

## 3. Solution

Regain detects a consented inbound lead (missed call, web form, ad lead form, opted-in CRM record), calls the person back within ~60 seconds in the business's own cloned rep voice, qualifies them using the business's own script and playbook, books an appointment directly into the calendar, and logs every lead and outcome in a revenue-tracking ledger. The owner watches live transcripts, can take over any call, and sees recovered revenue as the headline metric. If a call fails or the AI is uncertain, the system falls back to texting the lead and alerting a human so a lead is never silently dropped.

## 4. Goals and success metrics

**Product goals**
- Achieve sub-60-second median time-to-first-contact on consented leads.
- Make recovered revenue visible and trustworthy enough to justify the subscription on a single saved lead.
- Build switching cost through CRM integration and accumulated lead history.

**Success metrics (north stars)**
- Median time-to-first-contact (target: under 60s).
- Recovery rate (recovered leads / recoverable leads).
- Booked appointments per customer per month.
- Net revenue recovered per customer (estimated, customer-anchored math).
- Logo retention / monthly churn (target: under 5% monthly, given the category averages 15 to 25% in year one).

## 5. Target market

**Beachhead:** US home-services contractors (roofing, HVAC, plumbing, electrical), single-location and small multi-crew operators, where lead value is high and follow-up is poor.

**Why this segment:** high deal values ($800 to $40,000+), severe after-hours gap, ad-driven lead flow, and a documented willingness to buy speed-to-lead tools.

**Strategic note:** the broad "AI speed-to-lead for US home services" category already has a leader (LeadTruffle) and funded incumbents (Podium). Regain must win a defensible wedge: one trade in one region reachable through the founder's network, or an underserved geography (emerging-market SMBs that US tools ignore), not the whole category at once.

## 6. Personas

### Persona 1 — Marcus, the owner-operator (primary buyer and user)
- 38, owns a 6-person roofing company. On rooftops or driving most of the day.
- Pain: misses calls and form leads while working; competitors call back first; he has paid for ads that convert poorly.
- Goal: stop losing jobs without hiring an office manager he can't afford.
- Tech comfort: low to medium. Lives on his phone. Will not configure prompts or read docs.
- What wins him: a clear number showing recovered revenue, setup in minutes, and an app that pings him when a big job comes in.

### Persona 2 — Dana, the office manager / CSR (secondary user, potential blocker)
- 45, answers phones and books jobs for a small HVAC company.
- Pain: drowning during peak season; can't answer every call; manual data entry into the CRM.
- Fear: that AI is here to replace her. This fear can kill adoption if ignored.
- Goal: stop dropping calls during surges and stop re-typing lead details.
- What wins her: the AI handles routine overflow and after-hours, escalates anything complex or emotional to her, and writes clean records into the CRM so she stops doing data entry. Position the product as her assistant, not her replacement.

### Persona 3 — Tyler, the cloned rep (voice subject)
- 29, the company's best closer. His voice is what gets cloned.
- Concern: consent and control over his own voice.
- Requirement: must explicitly authorize cloning of his voice, see where it's used, and be able to revoke it if he leaves.

### Persona 4 — Priya, the homeowner (end recipient of the call, not a buyer)
- 41, submitted a "request a quote" form for a roof replacement, or called and got voicemail.
- Expectation: a fast, natural, helpful callback. Will judge the business by it.
- Requirement: the call must sound natural, respect that she consented, disclose recording where required, and hand off to a human if her situation is urgent or complex. A robotic or pushy call damages the customer's brand, which churns the customer.

### Persona 5 — Sofia, the multi-location operator (expansion persona)
- 50, owns 3 branches. Needs per-location settings, separate numbers, and roll-up reporting.
- Relevant for the business-switcher and roll-up analytics, not for MVP.

## 7. Positioning

Not "an AI that makes phone calls." Regain is **an AI lead recovery and revenue capture system**. The product is sold on recovered revenue and on never dropping a lead, not on the novelty of AI voice. Tone is calm, precise, and trustworthy, closer to a financial tool than a hype startup.

## 8. Scope

**In scope (v1 + roadmap):** consented outbound callback, voice cloning with consent, qualification, calendar booking, leads ledger, live transcript + human takeover, reliability/fallback layer, revenue tracking, AI training, follow-up sequences, high-value alerts, CRM sync.

**Explicitly out of scope:** cold calling of non-consented strangers (illegal under TCPA), purchased/scraped lists, autonomous "closing" of deals without human involvement on complex jobs, and any calling without a documented consent basis.

## 9. Feature requirements

Priority key: **P0** = MVP, must ship first. **P1** = fast follow after first paying customers. **P2** = later value/retention layer.

### 9.1 Lead intake
- P0: Website form webhook captures leads and inserts them into the ledger as `new`.
- P0: Missed inbound call capture triggers a recovery callback.
- P1: Ad lead-form intake (Google, Facebook/Meta lead ads).
- P1: Directory lead intake (Angi, Thumbtack, etc.) where consent exists.
- P0: Consent basis recorded for every lead source. No source without a consent basis is callable.

### 9.2 AI calling engine
- P0: Outbound call placed within ~60 seconds of a consented lead arriving.
- P0: Call uses the business's cloned rep voice.
- P0: Lead context (everything known about the lead) injected into the call.
- P0: Configurable qualifying questions per business.
- P0: Booking rules and availability honored on the call.
- P0: Post-call summary (one-line outcome) and full transcript saved.
- P1: Text-first-then-call sequencing option (mitigates Apple AI call screening of unknown numbers and improves recall).

### 9.3 Live call experience
- P0: Live streaming transcript during active calls with an in-progress indicator.
- P0: "Take over call" human handoff control.
- P0: Live call status and lead context shown alongside the transcript.

### 9.4 Reliability and escalation layer (load-bearing, build into architecture from day one)
- P0: Per-call confidence check. Low-confidence or failed calls trigger fallback.
- P0: Graceful failure: if the AI call fails, stalls, or is low-confidence, the system immediately texts the lead and alerts a human. A lead is never silently dropped.
- P0: Smart escalation: emergencies, complex scheduling, and emotionally sensitive calls route to a human rather than the AI bluffing through them.
- P1: Uptime and failure monitoring surfaced to the operator (because Regain is a wrapper on third-party voice infra, reliability transparency is a feature, not a backend detail).

### 9.5 Leads ledger (the spine)
- P0: Single leads table with: id, business_id, created_at, name, phone, email, source, lead_data (jsonb), status, appointment_at, calendar_event_id, transcript, call_summary, consent_basis.
- P0: Status lifecycle: new → calling → booked / no_answer / not_interested → won / lost, plus recovered.
- P0: Filterable list (All / Live / Booked / Recovered / No answer / New).
- P0: Lead detail view with full record, timeline of events, and transcript.
- P0: Add note to a lead.
- P1: Lead value field feeding revenue math.

### 9.6 Calendar and booking
- P0: Calendar connection via Cal.com (Google/Outlook underneath).
- P0: AI reads open slots and offers them on the call.
- P0: Booked event written back; event ID stored for reschedule/cancel.
- P0: Booked-appointment confirmation shown in the lead record.

### 9.7 AI training (how the AI sells)
- P1: Plain-language settings (no prompt writing) for services, service area, price ranges, qualifying questions, booking rules, and "never say" rules. The system assembles the prompt behind the scenes, with sensible per-vertical defaults.
- P1: "Test call to my own phone" button so changes are heard immediately.
- P2: Upload your own playbook/scripts/call notes as a knowledge base the AI references. Frame as the customer's own material to avoid ingesting copyrighted books verbatim.

### 9.8 Voice roster (whose voice it uses)
- P0: Clone one rep voice during onboarding with explicit consent.
- P1: Multiple cloned voices per business; assign which voice handles which lead type.
- P0: Per-voice consent record tied to the named person; ability to revoke and delete a voice.

### 9.9 Missed call recovery
- P1: Missed inbound call triggers automatic callback with timing shown (missed 2:13 → called back 2:14).
- P1: Completed-form-no-response triggers callback.
- P1: Recovered-leads count surfaced on dashboard.
- Guardrail: never call on abandoned/unsubmitted forms (no consent).

### 9.10 Follow-up sequences
- P2: Multi-step sequence (e.g., Day 0 call, Day 1 SMS, Day 3 call, Day 5 SMS, Day 7 final).
- P2: All activity logged to the ledger; per-step performance metrics.
- Guardrail: SMS steps require their own consent (TCPA), A2P 10DLC registration, and opt-out keyword handling (STOP/QUIT/CANCEL and variants).

### 9.11 High-value lead alerts
- P1: AI scores/flags high-value leads (deal size, keywords like "commercial").
- P1: Instant owner notification via push, SMS, and email.
- P1: High-value flag visible in ledger and dashboard.

### 9.12 Revenue and analytics
- P1: Dashboard with recovered revenue as the hero metric, plus recovery rate, booking rate, revenue missed, and follow-up conversion.
- P1: Trend over time.
- P0 (rule, applies whenever any figure is shown): every currency and percentage either traces to a real logged event or is labeled `est.` with a visible formula. Estimates are built from the customer's own average deal value and close rate, captured at onboarding. No fabricated numbers.

### 9.13 CRM integration (primary retention moat)
- P2: Two-way sync with one field-service CRM first (Jobber or Housecall Pro for SMBs; ServiceTitan for larger), then expand. Writes leads, calls, transcripts, and booked jobs into the customer's existing system so they stop doing manual entry and switching away means losing their pipe.

### 9.14 Onboarding and setup
- P0: 5-step wizard: business profile (industry, avg deal value, close rate) → connect lead sources → connect calendar → voice setup + consent → review and go live, with progress indicator.

### 9.15 Settings and account
- P0: Edit business profile, voice, calendar, lead sources, and business numbers.
- P0: Compliance section: consent records, recording disclosure, do-not-call list, audit log.
- P1: Business switcher (multi-location).
- P0: User account/avatar.

### 9.16 Notifications
- P1: In-app high-value alert banner, notification bell with unread indicator, toasts for key events, mobile push.

## 10. Non-functional requirements

- **Latency:** outbound callback initiated within ~60 seconds of lead arrival; in-call response latency low enough to feel natural (dependent on voice infra).
- **Reliability:** graceful degradation is mandatory (see 9.4). Target meaningful uptime despite third-party dependencies; surface failures rather than hide them.
- **Security:** no storage of payment credentials, SSNs, or similar; encrypted lead data; scoped per-business access.
- **Accessibility:** real focus states, aria labels, sufficient contrast in light and dark mode.
- **Responsiveness:** fully usable on a phone; primary user operates from mobile.

## 11. Compliance and legal (non-negotiable)

- **TCPA:** Regain only calls contacts with a documented consent basis (form submission requesting contact, missed inbound call, opted-in CRM record, ad lead form). It must never call purchased, scraped, or non-consented numbers. AI-generated/cloned voices count as "artificial voice" under the TCPA, so consent is the line that keeps the product legal.
- **Voice cloning consent:** each cloned person must explicitly authorize the clone of their own voice, with a per-voice consent record and revocation/deletion.
- **Recording disclosure:** handle call-recording disclosure per applicable state law (some states require two-party consent).
- **SMS:** any SMS follow-up requires its own consent, A2P 10DLC registration, and opt-out handling.
- **Do-not-call:** maintain and scrub against a DNC list; keep an audit log of calls and outcomes.

## 12. Technical architecture (high level)

- **Client:** Expo (React Native). Web build first for demos and early customers; native iOS/Android next for reliable push. One codebase.
- **Backend:** Supabase (Postgres, auth, storage) as the system of record (the ledger).
- **Orchestration:** edge functions / a worker reacting to lead webhooks; triggers calls and follow-ups.
- **Voice infra:** rented from Vapi or Retell (Regain is a wrapper; reliability layer in 9.4 exists because of this).
- **Voice cloning:** ElevenLabs or equivalent, gated by consent records.
- **Calendar:** Cal.com.
- **Notifications:** push (native), plus SMS/email providers.

## 13. Business model

- Flat subscription, $300 to $1,000 per month per business, anchored to recovered revenue so one saved lead pays for the subscription.
- Flat pricing deliberately avoids the under-$50 churn death zone and the per-lead pricing that punishes high-volume customers.

## 14. Platform and go-to-market

- Build in Expo. Use the web build for demos and the first handful of customers (send a link, no install, prove ROI fast). Graduate to native iOS/Android for the real product once paying customers exist, when reliable push starts driving retention.
- GTM is direct B2B: the founder onboards each customer. No reliance on app-store discovery.
- Win a specific reachable wedge first (one trade/region via network, or an underserved geography), not the whole category.

## 15. Risks and mitigations

- **Crowded market with a direct competitor (LeadTruffle) and funded incumbents (Podium).** Mitigation: compete on a wedge they can't reach, plus the reliability and recovered-revenue framing.
- **Churn (category averages 15 to 25% monthly in year one; AI products churn fast).** Mitigation: visible ROI (revenue tracker) plus sticky CRM integration (clients with 4+ integrations churn ~73% less).
- **Wrapper reliability (stacked third-party failure points).** Mitigation: the graceful-failure layer in 9.4, plus failure transparency.
- **Apple AI call screening intercepting unknown-number calls (2026).** Mitigation: text-first-then-call sequencing option (9.2).
- **Legal exposure if consent discipline slips.** Mitigation: consent basis enforced at the data layer; no callable lead without it.
- **Customer-brand damage from a robotic or pushy AI call.** Mitigation: natural voice, smart escalation, honest "we catch our own misses" framing.

## 16. Release plan

- **Phase 0 — MVP (P0):** lead intake (form + missed call), AI callback in cloned voice, qualification, Cal.com booking, leads ledger, live transcript + takeover, reliability/fallback layer, onboarding wizard, compliance basics. Ship the web build for demos and first customers.
- **Phase 1 — fast follow (P1):** revenue dashboard, high-value alerts, AI training screen, missed-call-recovery surfacing, ad/directory lead intake, text-first sequencing, native apps with push.
- **Phase 2 — retention and depth (P2):** follow-up sequences, playbook upload, multi-voice roster, CRM two-way sync, multi-location.

## 17. Open questions

- Which exact vertical and geography is the beachhead, given distribution is the deciding factor?
- Which CRM to integrate first (Jobber vs Housecall Pro vs ServiceTitan), driven by what the first 10 customers actually use?
- Voice + STT + TTS stack final choice and its real-world in-call latency.
- Default qualification script per vertical: who writes the first one?
