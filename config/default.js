const config = {
  "team_name": process.env.TEAM_NAME,
  "contact_email": process.env.CONTACT_EMAIL,

  "host": "::",
  "port": process.env.PORT,
  "endpoint": "https://" + process.env.PROJECT_DOMAIN + ".glitch.me",
  "invite_code": process.env.INVITE_CODE,

  "storage_dialect": "sqlite",

  "storage_host": "localhost",
  "storage_database": "spacedeck",
  "storage_username": "username",
  "storage_password": "password",

  "storage_local_path": "./.data",
  "storage_local_db": "./.data/database.sqlite",
  "storage_region": "eu-central-1",
  "storage_endpoint": "http://localhost:4572",
  "storage_bucket": "my_spacedeck_bucket",
  "storage_cdn": "/storage",

  "mongodb_host": "localhost",
  "redis_mock": true,
  "redis_host": "localhost",

  "export_api_secret": process.env.EXPORT_API_SECRET,

  "mail_provider": "smtp",
  "mail_smtp_host": "your.smtp.host",
  "mail_smtp_port": 465,
  "mail_smtp_secure": true,
  "mail_smtp_require_tls": true,
  "mail_smtp_user": "your.smtp.user",
  "mail_smtp_pass": "your.secret.smtp.password",
  
  "spacedeck": {
    "default_text_color": "#E11F26",
    "default_stroke_color": "#9E0F13",
    "default_fill_color": "#64BCCA",
    "swatches": [
      {"id":8, "hex":"#000000"},
      {"id":30, "hex":"rgba(0,0,0,0)"},
      {"id":31, "hex": "#E11F26"},
      {"id":32, "hex": "#9E0F13"},
      {"id":33, "hex": "#64BCCA"},
      {"id":34, "hex": "#40808A"},
      {"id":35, "hex": "#036492"},
      {"id":36, "hex": "#005179"},
      {"id":37, "hex": "#84427E"},
      {"id":38, "hex": "#6C3468"},
      {"id":39, "hex": "#F79B84"},
      {"id":40, "hex": "#B57362"},
      {"id":41, "hex": "#E7D45A"},
      {"id":42, "hex": "#ACA044"}
    ]
  },
  
  "db_logs_disabled": true,
};

module.exports = config;