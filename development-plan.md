# Development Plan

**Purpose:** A simple, low-risk approach for a solo developer to build and sell Whisper Lite.

**Philosophy:** Build something you want to use, share it with the world, see what happens.

---

## Phase 1: Just Build It

**Focus:** Create a working product you personally want to use.

**No business setup needed.** Just build.

### Priorities
1. Build the core product (recording → transcription → history)
2. Use it yourself daily
3. Iterate based on your own needs

---

## Phase 2: When Ready to Sell

### Minimum Requirements

| Item | Cost | Notes |
|------|------|-------|
| Apple Developer Program | $99/year | Required for signed macOS distribution |
| Simple website | $0-50/year | GitHub Pages (free) or domain (~$12/year) |
| Payment processor | % of sales | Gumroad, Paddle, or LemonSqueezy handle taxes |

**Total startup cost:** ~$100-150

### Payment Processor Recommendations

| Service | Cut | Handles Tax | Notes |
|---------|-----|-------------|-------|
| Gumroad | 10% | Yes | Simplest, good for starting |
| Paddle | 5-10% | Yes | Better rates, acts as reseller |
| LemonSqueezy | 5-8% | Yes | Modern, developer-friendly |
| Stripe | 2.9% | No | Lower fees but you handle tax |

**Recommendation:** Start with Gumroad or Paddle. They act as "Merchant of Record" meaning they handle VAT, sales tax, refunds, and payment disputes. Worth the extra fee for simplicity.

### Suggested Pricing

| Approach | Price | Notes |
|----------|-------|-------|
| Simple one-time | $29-39 | Easy to understand, no ongoing obligation |
| Pay what you want | $0+ suggested $25 | Lower barrier, some pay more |
| Open source + donations | $0 | Maximum reach, uncertain revenue |

---

## Phase 3: If It Makes Money

Once you're making consistent revenue ($5k-10k+/year), consider:

| Item | Cost | Why |
|------|------|-----|
| LLC formation | $50-500 | Separates personal assets from business |
| Business bank account | $0-10/month | Keep finances separate |
| Basic insurance | ~$500/year | Extra liability protection |
| Accountant (1x/year) | $200-500 | Ensure taxes done correctly |

### LLC Formation Options

| Service | Cost | Notes |
|---------|------|-------|
| State website directly | $50-150 | Cheapest, varies by state |
| ZenBusiness | $0 + state fee | Free tier available |
| Stripe Atlas | $500 | Premium, includes bank account |

**Recommendation:** Wait until you have revenue. Form in your home state. Delaware/Wyoming are popular but add complexity if you don't live there.

---

## What You Can Skip

| Item | Why Skip |
|------|----------|
| LLC (initially) | Not needed until making real money |
| Lawyer | Standard EULA templates work for low-risk software |
| Accountant (initially) | Payment processors provide tax docs |
| SOC 2, ISO 27001, HIPAA | Only for enterprise/healthcare markets |
| Detailed market research | You're your own first customer |
| Complex business plan | Build first, plan later |

---

## Risk Mitigation (No Lawyer Needed)

### Low-Risk Product Characteristics

Whisper Lite has a favorable risk profile:

- **Offline-only** — No data breaches possible
- **No user accounts** — No credential theft
- **No cloud storage** — No server liability
- **User-managed models** — User responsible for whisper.cpp
- **Local processing** — Data never leaves user's machine

### Simple Protections

1. **Include a EULA/Terms of Service**
   - Use a template (many available online)
   - Key clause: "Software provided as-is, no warranty"
   - Key clause: "Not liable for data loss or damages"

2. **Include a Privacy Policy**
   - Simple: "We collect no data. Everything stays on your machine."

3. **Honest Marketing**
   - Don't claim medical/legal accuracy
   - Don't claim enterprise security certifications you don't have
   - Be clear about what it does and doesn't do

4. **Use Merchant of Record payment processor**
   - They handle legal liability for transactions
   - They handle refunds and disputes
   - They handle international tax compliance

---

## Launch Checklist

### Pre-Launch
- [ ] Working product you use daily
- [ ] Apple Developer account ($99)
- [ ] Code signing and notarization working
- [ ] Simple landing page with screenshots
- [ ] Payment processor account (Gumroad/Paddle)
- [ ] Basic EULA and privacy policy
- [ ] README with clear installation instructions

### Launch
- [ ] Post to Hacker News (Show HN)
- [ ] Post to relevant subreddits (r/macapps, r/productivity)
- [ ] Tweet/post about it
- [ ] Submit to Product Hunt (optional)

### Post-Launch
- [ ] Monitor for feedback
- [ ] Fix critical bugs quickly
- [ ] Collect testimonials from happy users
- [ ] Iterate based on feedback

---

## Revenue Expectations (Realistic)

| Outcome | Monthly Revenue | Likelihood |
|---------|-----------------|------------|
| Modest success | $100-500 | Common |
| Good indie product | $500-2,000 | Possible with marketing |
| Hit product | $2,000-10,000 | Rare, requires luck/timing |
| Breakout success | $10,000+ | Very rare |

**Most indie products:** Make enough to cover costs and provide some side income. That's a success.

---

## Resources

### Templates
- EULA Generator: https://www.eulatemplate.com/
- Privacy Policy Generator: https://www.privacypolicygenerator.info/

### Distribution
- Apple Developer: https://developer.apple.com/programs/
- Gumroad: https://gumroad.com/
- Paddle: https://www.paddle.com/

### Community
- Indie Hackers: https://www.indiehackers.com/
- r/SideProject: https://www.reddit.com/r/SideProject/
- r/macapps: https://www.reddit.com/r/macapps/

