# Aetherneum Sites

Static-site assets for the Aetherneum brand pillar, served by an Nginx
container behind Traefik on the host machine.

## Layout

- `aetherneum-com/` — main site at `aetherneum.com`
- `university-aetherneum-com/` — the University site at `university.aetherneum.com`
- `scripts/update-activity.py` — Live Activity feed generator (cron every 10 min)
- `nginx.conf` — Nginx config served by the container
- `docker-compose.yml` — container definition (Nginx 1.27 alpine, read-only volumes)

## Activity feed

The Live Activity section on the University homepage is rebuilt every 10 minutes
by `scripts/update-activity.py`, which pulls recent commits across
`aetherneum-network/*` via the GitHub REST API (anonymous, 60 req/h cap).

This repository ships the **placeholder** version of the feed block. The live
generated content is not committed back — it would be noisy and add nothing.

## Per Æthera Ad Astra.
