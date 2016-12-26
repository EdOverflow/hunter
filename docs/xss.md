# Cross-site scripting (XSS)

Cross-site scripting (XSS) is a form of client-side code injection wherein one can execute malicious scripts into a page. XSS exists whenever input can be interpreted as code. In order to prevent XSS all input should be escaped server-side.

Cross-site scripting can be divided into 3 categories:

* Reflected XSS
* Stored XSS
* Self-XSS

## Reflected XSS

Reflected XSS is non-persistent and executes in form of a request.

For example, you may see the following:

~~~
https://example.com/page?url=value
~~~

This vulnerable website does not escape nor validate the input and it is simply placed inside a link:

~~~
<a href={{ url }}>Link</a>
~~~

Now if one submits the following we are prompted with an alert box display the value `1`:

~~~
onload=alert(1)
~~~

## Stored XSS

As the name already suggests, stored XSS means that the payload is stored in the page, for example, in form of a comment. This [self-retweeting tweet](https://twitter.com/dergeruhn/status/476764918763749376) used a stored XSS vulnerability to force people loading the page to retweet the tweet. 

The payload looked as follows:

~~~
<script class="xss">
	$('.xss').parents().eq(1).find('a').eq(1).click();
	$('[data-action=retweet]').click();
	alert('XSS in Tweetdeck')
</script>♥
~~~

If you would like to find out how this payload works, please refer to the fantastic video by Tom Scott.

[![self-retweeting tweet](https://i.ytimg.com/vi/zv0kZKC6GAM/maxresdefault.jpg)](https://www.youtube.com/watch?v=zv0kZKC6GAM)

The [Samy worm](https://samy.pl/popular/tech.html) was also a form of stored XSS in MySpace.

## Self-XSS

Self-XSS requires an attacker to convince (social engineer) the victim into executing the XSS. This form of XSS can neither be sent in form of a URL nor stored in a page.

## XSS mitigations

Django escapes certain characters by default, but there are exceptions which you should read up on here: https://docs.djangoproject.com/en/1.10/topics/security/#cross-site-scripting-xss-protection

In the case of Flask, they have implemented [Jinja2](http://jinja.pocoo.org/docs/dev/templates/#html-escaping) to escape input: http://flask.pocoo.org/docs/0.12/security/#cross-site-scripting-xss

In both frameworks it is very important to note that the mitigations put in place will not protect against attribute injection. Therefore, be sure to always quote your attributes with either double or single quotes.

### 👎 Don't do this

`<a href={{ url }}>Link</a>`

### 👍 Use this instead

`<a href="{{ url }}">Link</a>`

In particular, the Django docs demonstrate that it is possible to inject `'classname onmouseover=javascript:alert(1)'` into unquoted class attributes.

~~~
<style class={{ var }}>...</style>
~~~

If you would rather directly implement Jinja2, you can manually escape HTML by passing a value through `|e`.

~~~
{{ url|e }}
~~~ 

Another method is to escape with the `escape()` function.

~~~
>>> from jinja2 import utils
>>> str(utils.escape("<h1>XSS</h1>"))
'&lt;h1&gt;XSS&lt;/h1&gt;'
~~~
