# Dark Mode

## SCSS @mixin with `<body class="dark-mode">`

```scss
@mixin dark-mode {
  @if & {
    @at-root body.dark-mode & {
      @content;
    }
  } @else {
    @at-root body.dark-mode {
      @content;
    }
  }
}
```

#### Usage1 - not top-level & content contains selectors
```scss
.my-class {
  color: blue;
  .my-class1 {
    color: white;
  }
  @include dark-mode {
    color: gray;
    .my-class1 {
      color: black;
    }
  }
}

// Output:
.my-class {
  color: blue;
}
.my-class .my-class1 {
  color: white;
}
body.dark-mode .my-class {
  color: gray;
}
body.dark-mode .my-class .my-class1 {
  color: black;
}
```

#### Usage2 - not top-level & content only contains rules
```scss
.my-class {
  color: blue;
  @include dark-mode {
    color: red;
  }
}

// Output:
.my-class {
  color: blue;
}
body.dark-mode .my-class {
  color: red;
}
```

#### Usage3 - top-level & content contains selectors
```scss
@include dark-mode {
  .my-class {
    color: red;
  }
}

// Output:
body.dark-mode .my-class {
  color: red;
}
```

#### Usage4 - top-level & content only contains rules
```scss
@include dark-mode {
  color: red;
}

// Output:
body.dark-mode {
  color: red;
}
```
