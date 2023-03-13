# Vertical align center with scroll

::: warning Known issue
The scrollbar will always be displayed.
:::

## Preview

<video src="/assets/media/vertical-align-center.mp4" autoplay="true" controls="true" loop="true" muted="true"></video>

## Code

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Vertical Align Center</title>
  <style>
    html, body {
      width: 100%;
      height: 100%;
      padding: 0;
      margin: 0;
    }
    #container {
      display: block;
      height: 100%;
	    overflow-y: scroll;
    }
    #container:before {
      display: inline-block;
      width: 0;
      height: 100%;
      vertical-align: middle;
      content: "";
    }

    #wrapper {
      display: inline-block;
	    vertical-align: middle;
	    width: calc(100vw - 32px);
    }
    p {
      height: 100px;
      width: 400px;
      margin: 0 auto;
    }
    p:nth-child(odd) {
      background: rgb(194, 194, 194);
    }
  </style>
</head>
<body>
  <div id="container">
    <div id="wrapper">
      <p>Something 1</p>
      <p>Something 2</p>
      <p>Something 3</p>
      <p>Something 4</p>
      <p>Something 5</p>
    </div>
  </div>
</body>
</html>
```