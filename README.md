# Keyfresh-Site

Simple website written in `Pugjs`, `Sass`, and `Python`. Built using `Gulp`.
Backed by `MongoDB`. Hosted with `Flask` + `uwsgi` + `Nginx`.


## Gulp: Jinja vs Pugjs

Webpage source is written in Pug. However, with `pypugjs`, it compiles to
`jinja` at runtime to be used with Flask. The plugin handles most of this
well, however, stumbles when it comes to converting paths to the required
static location format.

To mitigate this, all local paths in pug must still use the `{{url_for(...)}}`
notation native to `jinja` in the `.pug` files.
