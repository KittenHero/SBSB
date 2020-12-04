CC=npm run build --

BUILDPATH=build/
SRCDIR=src/
HTML=$(BUILDPATH)index.html
HTMLSRC:=$(shell find $(SRCDIR) -name '*.pug')
CSS=$(BUILDPATH)styles.css
CSSSRC:=$(shell find $(SRCDIR) -regex '.*\\.\\(pug\\|css\\|js\\)')
ASSETSSRC:=$(shell find $(SRCDIR) -regex '.*\\.\\(js\\|png\\|jpg\\|svg\\|ico\\)')
ASSETS:=$(subst $(SRCDIR), $(BUILDPATH), $(ASSETSSRC))
BUILDSUBDIRS:=$(shell echo $(dir $(ASSETS))|tr ' ' '\n'|sort -u|tr '\n' ' ')
S3BUCKET:=s3://sabaisabaithaimassage.com.au

.PHONY: all clean

all: $(HTML) $(CSS) $(ASSETS)

clean:
	rm -rf $(BUILDPATH)

$(HTML): $(HTMLSRC) | $(BUILDPATH)
	@echo $@
	@$(CC) -html

$(CSS): $(CSSSRC) | $(BUILDPATH)
	@echo $@
	@$(CC) -css

$(BUILDSUBDIRS):
	@mkdir -p $@

.SECONDEXPANSION:

$(BUILDPATH)%.jpg: $(SRCDIR)%.jpg | $(BUILDSUBDIRS)
	@echo $@
	@cp $< $@

$(BUILDPATH)%.png: $(SRCDIR)%.png | $(BUILDSUBDIRS)
	@echo $@
	@cp $< $@

$(BUILDPATH)%.svg: $(SRCDIR)%.svg | $(BUILDSUBDIRS)
	@echo $@
	@cp $< $@

$(BUILDPATH)%.ico: $(SRCDIR)%.ico | $(BUILDSUBDIRS)
	@echo $@
	@cp $< $@

$(BUILDPATH)%.js: $(SRCDIR)%.js | $(BUILDSUBDIRS)
	@echo $@
	@cp $< $@
