## API Orchestration 

This is a python package currently used as an inhouse solution
to manage and orchestration various API calls where integrations
to a SIEM are limited, or where a custom API call is desired.

These API calls can store results in either a flat file, SQLite or Elastic. 

Why not just cURL? Well, you can do that, but when you're dealing with a larger set 
of custom API calls you might want to abstract that repetition out of long cURL strings. Instead
the API calls can be constructed a lot like a YAML. In fact, a yaml config is likely to come.

Currently this development on this is taking a backseat to other projects.
