var gulp = require('gulp');
var pug = require('gulp-pug');
var sass = require('gulp-sass');

var html_dest = 'server/app/static/templates';
var sass_test = "server/app/static/css";

// Compiles .pug files into .html
gulp.task('pug', function() {
	gulp.src('src/**.pug')
		.pipe(pug())
		.pipe(gulp.dest(html_dest)); // tell gulp our output folder
});

// Compiles .sass into .css
gulp.task('sass', function() {
	gulp.src('src/sass/**.sass')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest(sass_dest));
});

//
gulp.task('build', ['pug', 'sass']);

// Monitors .pug and .sass
gulp.task('watch', function() {
	gulp.watch('src/**', ['pug', 'sass']);
});

//
gulp.task('default', function() {
  	// place code for your default task here
	console.log("Hi, I'm Gulp!")
});
