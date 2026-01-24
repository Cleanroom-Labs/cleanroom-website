# Website Migration Plan: Articulation to Next.js with Vercel

## Migration Progress

### Phases 1-4: ✅ Complete
- Project setup, build integration, core pages
- SEO: robots.txt, sitemap generation via `next-sitemap`

### Phase 5: CI/CD ❌ Not Started
- [ ] Create `.github/workflows/quality-checks.yml`
- [ ] Verify CI builds with artifact checks

### Phase 6: Vercel Deployment ❌ Not Started
- [ ] Create Vercel account and import repo
- [ ] Configure build settings (Build: `npm run build`, Node 18+)
- [ ] Verify preview deployment works

### Phase 7: Domain Setup ❌ Not Started
- [ ] Add `cleanroomlabs.dev` in Vercel domains
- [ ] Update DNS in Porkbun (A record: `@` → `76.76.21.21`, CNAME: `www` → `cname.vercel-dns.com`)
- [ ] Verify SSL certificate issued

### Phase 8: Monitoring & Launch ❌ Not Started
- [ ] Add Vercel Analytics (`@vercel/analytics`)
- [ ] Add Sentry error monitoring (`@sentry/nextjs`)
- [ ] Deploy to production and verify

---

## Quick Reference

| Phase | Task | Guide |
|-------|------|-------|
| 5 | CI/CD | [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) |
| 6-7 | Deployment & Domain | [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) |
| 8 | Monitoring | [Vercel Analytics](https://vercel.com/docs/analytics), [Sentry Docs](https://docs.sentry.io/platforms/javascript/guides/nextjs/) |

## Rollback Plan

If critical issues occur after launch: Vercel dashboard → find last working deployment → "..." → "Promote to Production"

---

## Related Documentation

- [maintenance-plan.md](maintenance-plan.md) - Post-launch improvements (testing, TypeScript, staging)
- [README.md](README.md) - Getting started and build commands
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design decisions
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues
