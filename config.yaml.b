appName: monocle
logLevel: WARN

API:
  Proofpoint:
    Url: 'https://tap-api-v2.proofpoint.com/v2/siem/'
    Creds:
      Token: "a737f3cb-8c8e-d873-086b-270540dcab5d"
      Secret: "f298519077c461d214e9b615e8c3515e35f5b1079a73c90f62caacf9ddacddf0"

routes:
  admin:
    url: /admin
    template: /admin.html
    assets:
      templates: /templates
      static: /static
  dashboard:
    url: /dashboard
    template: dashboard.html
    assets:
      templates: /templates
      static: /static

database:
  sqlite:
    host: hostname
    username: admin
    password: admin




