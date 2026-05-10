# Troubleshooting Guide

## Dashboard cannot reach API

Check:
- Cloud Run deployment status
- CORS configuration
- Vercel environment variables

## Redis queue failing

Check:
- REDIS_URL
- local Redis container
- queue health endpoint

## Eval gate always returns HOLD

Check:
- retrieval_hit_rate
- missing evidence
- conflicting context

## Tool-call failures

Inspect:
- tool_errors
- trace_id
- support-decision audit logs
