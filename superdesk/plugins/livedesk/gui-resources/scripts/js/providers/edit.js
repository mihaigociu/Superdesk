/*  * To change this template, choose Tools | Templates * and open the template in the editor. */define('providers/edit', [	'providers',	'utils/str',	'jquery',    'jquery/rest',    'jquery/superdesk',    'jquery/tmpl',	'jqueryui/draggable',    'jqueryui/texteditor',	'providers/edit/adaptor',    'tmpl!livedesk>providers/edit',    'tmpl!livedesk>providers/edit/item',], function( providers, str, $ ) {	$.extend(providers.edit, {        data: [],        init: function(theBlog) {            var            editorImageControl = function()            {                // call super                var command = $.ui.texteditor.prototype.plugins.controls.image.apply(this, arguments);                // do something on insert event                $(command).on('image-inserted.text-editor', function()                {                    var img = $(this.lib.selectionHas('img'));                    if( !img.parents('figure.blog-image:eq(0)').length )                        img.wrap('<figure class="blog-image" />');                });                return command;            },            editorTitleControls = $.extend({}, $.ui.texteditor.prototype.plugins.controls, { image : editorImageControl }),            initEdit = function(theBlog) {                var content = $(this).find('[is-content]'),                    h2ctrl = $.extend({}, $.ui.texteditor.prototype.plugins.controls);                delete h2ctrl.justifyRight;                delete h2ctrl.justifyLeft;                delete h2ctrl.justifyCenter;                delete h2ctrl.html;                delete h2ctrl.image;                delete h2ctrl.link;                content.find('article').texteditor                ({                    plugins:{ controls: editorTitleControls },                    floatingToolbar: 'top'                });                $(this)                    .off('click.livedesk')                    .on( 'click.livedesk','[ci="savepost"]', function(e){                        e.preventDefault();                        var data = {                            Content: $('[name="body-text"]').val(),                            Type: $('[name="type"]').val(),                        };                        new $.restAuth(theBlog+'/Post').resetData().insert(data).done(function(post){                            $('[name="body-text"]').val('');                            $('[name="type"]').val('normal');                            updatePosts();                            new $.restAuth(post.href+'/Publish').resetData().insert().done(function(){                            });                        });                    })                    .on('click.livedesk','[ci="save"]',function(e){                        e.preventDefault();                        var data = {                            Content: $('[name="body-text"]').val(),                            Type: $('[name="type"]').val(),                        };                        new $.restAuth(theBlog+'/Post').resetData().insert(data).done(function(){                            $('[name="body-text"]').val('');                            $('[name="type"]').val('normal');                            updatePosts();                        });                    });                $('form').submit(function() {                    console.log($(this).serializeArray());                    return false;                });                updatePosts();            }, updatePosts = function(){                var postHref = theBlog+'/User/'+ $.superdesk.login.Id + '/Post',                    blog = new $.restAuth({                        postUnpublished: { href: postHref + '/Unpublished'},                        postPublished: {href: postHref + '/Published'}})                    .get('postUnpublished').xfilter('Id,AuthorName,Content,Type.Key,CreatedOn,Author.Source.Name')                    .get('postPublished').xfilter('Id,AuthorName,Content,Type.Key,CreatedOn,Author.Source.Name')                    .done(function(unpublished, published)                    {                        published = this.extractListData(published[0]);                        $.each(published, function(){ this.State = 'published';});                        unpublished = this.extractListData(unpublished[0]);                        $.each(unpublished, function(){ this.State = 'unpublished';});                        var postList = published.concat(unpublished);                        //$.tmpl('livedesk>providers/edit/item', {Posts: postList}, function(e,o){ console.log(o);});                        self.data = postList;                        self.el.find('#own-posts-holder')                        .tmpl('livedesk>providers/edit/item', {Posts: postList}, function(){                            $(this).find('li.unpublished,div.unpublished').draggable(                                {                                    revert: 'invalid',                                    containment:'document',                                    helper: 'clone',                                    appendTo: 'body',                                    zIndex: 2700,                                    clone: true,                                    start: function() {                                        var idx = parseInt($(this).attr('idx'),10);                                        //$(this).data('data', self.adaptor.universal(self.data[idx], $(this)));                                        $(this).data('post', self.adaptor.universal(self.data[idx], $(this)));                                    }                                }                            );                        }).end()                        .on('click.livedesk','.close',function(){                            /*                            new $.restAuth(postHref);                            */                        });                });                    self.el.find('.own-posts-results').tmpl('')            },self = this;            new $.restAuth('Superdesk/PostType').xfilter('Key').done(function(PostTypes){                self.el.tmpl('livedesk>providers/edit',{PostTypes: PostTypes},function(){                    initEdit.call(this, theBlog);               });            });		}			});	return providers;});