# Reverse Tabnabbing

The following <a href="https://edwinfoudil.com/hunter/demo/reverse-tabnabbing.html" target="_blank">link</a> is vulnerable to reverse tabnabbing, because it uses `target="_blank"`:

~~~
<a href="https://example.com/" target="_blank">link</a>
~~~

This means the page that opens in a new tab can access the initial tab and change its location using the `window.opener` property.

In order to mitigate this issue, developers are encouraged to use `rel="nofollow noopener noreferrer"` as follows:

~~~
<a href="https://example.com/" target="_blank" rel="nofollow noopener noreferrer">link</a>
~~~

Now when you click on this <a href="https://edwinfoudil.com/demo/code/reverse-tabnabbing.html" target="_blank" rel="nofollow noopener noreferrer">link</a>, the attacker cannot access the initial tab.

For more on reverse tabnabbing, please refer to the following page: https://www.jitbit.com/alexblog/256-targetblank---the-most-underestimated-vulnerability-ever/