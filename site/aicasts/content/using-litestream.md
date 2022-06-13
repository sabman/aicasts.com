---
title: "Using Litestream"
date: 2020-09-15T11:30:03+00:00
# weight: 1
# aliases: ["/first"]
tags: ["first"]
author: "Me"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: false
description: "Desc Text."
canonicalURL: "https://canonical.url/to/page"
disableHLJS: true # to disable highlightjs
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
    relative: false # when using page bundles set this to true
    hidden: true # only hide on current single page
editPost:
    URL: "https://github.com/<path_to_repo>/content"
    Text: "Suggest Changes" # edit text
    appendFilePath: true # to append file path to Edit link
---

```sh
brew install benbjohnson/litestream/litestream
```

```sh
# ==> Tapping benbjohnson/litestream
# Cloning into '/opt/homebrew/Library/Taps/benbjohnson/homebrew-litestream'...
# remote: Enumerating objects: 38, done.
# remote: Counting objects: 100% (38/38), done.
# remote: Compressing objects: 100% (16/16), done.
# remote: Total 38 (delta 10), reused 34 (delta 9), pack-reused 0
# Receiving objects: 100% (38/38), 4.34 KiB | 1.45 MiB/s, done.
# Resolving deltas: 100% (10/10), done.
# Tapped 1 formula (12 files, 9.9KB).
# ==> Downloading https://github.com/benbjohnson/litestream/releases/download/v0.3.8/litestream-v0.3.8-darwin-amd64.zip
# ==> Downloading from https://objects.githubusercontent.com/github-production-release-asset-2e65be/301830590/2d4fc6e6-3336-444e-9220-c31fa0c05dae?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWN
# ######################################################################## 100.0%
# ==> Installing litestream from benbjohnson/litestream
# 🍺  /opt/homebrew/Cellar/litestream/0.3.8: 3 files, 23.7MB, built in 1 second
# ==> Running `brew cleanup litestream`...
# Disable this behaviour by setting HOMEBREW_NO_INSTALL_CLEANUP.
# Hide these hints with HOMEBREW_NO_ENV_HINTS (see `man brew`).
```

```sh
litestream version8
```

```sh
# v0.3.8
```