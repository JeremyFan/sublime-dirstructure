# Sublime-DirStructure

This plugin helps you to generate a directory structure of a project, makes document more clear, and easy to edit and update.

```
.
├── dist
├── src
│   ├── css
│   └── js
├── server.js
└── package.json
```

## Install
Open sublime, go to `Preferences -> Browse packages...`, and download `dirstructure` to this directory:

```
git clone git@github.com:JeremyFan/sublime-dirstructure.git
```

## Config
Go to `Preferences -> Key Bindings`, and config a shortcut you like, for example `ctrl + shift + d`:

```
{
  "keys": ["ctrl+shift+d"],
  "command": "dir_structure"
}
```

## Using
### Basic
Just write the file name or folder name of the project, for example:

```
src
server.js
package.json
```

Selected these lines, and press `ctrl + shift + d` (or other shortcut you config),
then `dirstructure` generates:

```
.
├── src
├── server.js
└── package.json
```

### Sub Directory

Use **brackets**(`()`) for sub directory, and split them with a **comma**(`,`), for example:

```
dist
public(logos,fonts)
src(css,js(libs,api(index.js)),images)
server.js
package.json
```

`dirstructure` generates:

```
.
├── dist
├── public
│   ├── logos
│   └── fonts
├── src
│   ├── css
│   ├── js
│   │   ├── libs
│   │   └── api
│   │       └── index.js
│   └── images
├── server.js
└── package.json
```
You can nests any level of folder.

### Comment
If you want add some explain for a file or a folder, use **sharp**(`#`), for example:

```
dist#after build
public(logos,fonts)
src#source code(css,js(libs,api#api module(index.js)),images)
server.js
package.json
webpack.config.js#webpack config
```

`dirstructure` generates:

```
.
├── dist ···················· after build
├── public
│   ├── logos
│   └── fonts
├── src ····················· source code
│   ├── css
│   ├── js
│   │   ├── libs
│   │   └── api ············· api module
│   │       └── index.js
│   └── images
├── server.js
├── package.json
└── webpack.config.js ······· webpack config
```
Looks good, auto align for the comment text.

## Write Documents
Most of developers like use markdown to write documents for a project. If use this plugin to manager the description of directory structure, I recommend to reserve the raw code, in order to edit and generate next time.

For example, I use `<!-- -->` to comment and hide the raw code in document. When directory changes, I generate a new directory structure by raw code instead of the old one.