# Unified Configuration Reference

This document ensures all configuration values are consistent across the entire project.

## Standard Configuration

### RAT Server Configuration
- **Host:** `127.0.0.1` (update to your server IP)
- **Port:** `4444`
- **Encryption Key:** `YOUR_ENCRYPTION_KEY_HERE` (update before deployment)
- **API Port:** `5000`

### WhatsApp Bot Configuration
- **Bot Name:** `T0OL-B4S3-263 C2`
- **Command Prefix:** `/`
- **Owner Numbers:** Stored in `whatsapp-c2/config.json`

### Configuration Files Map

| File | Purpose | Config Values |
|------|---------|---|
| `whatsapp-c2/config.json` | Node.js bot main config | ratServer, whatsapp, features |
| `rat_api_bridge.py` | Flask API bridge | C2_SERVER_HOST, C2_SERVER_PORT, ENCRYPTION_KEY |
| `setup.py` | Interactive setup | Dynamic config generation |
| `rat_ultimate.py` | Ultimate RAT server | Embedded port configs |

## Configuration Update Protocol

1. **Update whatsapp-c2/config.json** - Master configuration file
2. **Run setup.py** - Will ask for configuration values
3. **Verify rat_api_bridge.py** - Check manual values match
4. **Check rat_ultimate.py** - Look for hardcoded values

## Environment Variables (Recommended for Production)

```bash
export RAT_SERVER_HOST=192.168.1.201
export RAT_SERVER_PORT=4444
export RAT_ENCRYPTION_KEY=your_key_here
export WHATSAPP_API_PORT=5000
```

## Validation Checklist

- [ ] All `ratServer.host` values match
- [ ] All `ratServer.port` values match (4444)
- [ ] All encryption keys match
- [ ] API port is consistent (5000)
- [ ] No hardcoded IP addresses in production code
- [ ] All config.json files valid JSON

