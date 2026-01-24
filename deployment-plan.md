# Deployment Plan

## Checklist

### CI/CD
- [ ] Create `.github/workflows/quality-checks.yml`
- [ ] Verify CI builds with artifact checks

### Vercel
- [ ] Create account and import repo
- [ ] Configure build settings (Build: `npm run build`, Node 18+)
- [ ] Verify preview deployment

### Domain
- [ ] Add `cleanroomlabs.dev` in Vercel
- [ ] Update DNS in Porkbun (A: `@` → `76.76.21.21`, CNAME: `www` → `cname.vercel-dns.com`)
- [ ] Verify SSL certificate

### Monitoring & Launch
- [ ] Add Vercel Analytics (`@vercel/analytics`)
- [ ] Add Sentry (`@sentry/nextjs`)
- [ ] Deploy to production

## References

| Task | Guide |
|------|-------|
| CI/CD | [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) |
| Deployment | [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) |

## Rollback

Vercel dashboard → find working deployment → "..." → "Promote to Production"

---

## Related Documentation

- [maintenance-plan.md](maintenance-plan.md) - Post-launch improvements (testing, TypeScript, staging)
- [README.md](README.md) - Getting started and build commands
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design decisions
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues
