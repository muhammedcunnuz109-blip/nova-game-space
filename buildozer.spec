[app]

title = Nova Game Space
package.name = novagamespace
package.domain = org.nova

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 0.1

requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23

android.permissions = android.permission.QUERY_ALL_PACKAGES

android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
