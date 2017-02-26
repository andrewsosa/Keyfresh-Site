var gulp = require('gulp');

var html_dest = 'flask/app/templates';
var sass_dest = "flask/app/static/css";

// Compiles .pug files into .html
gulp.task('pug', function() {
	var pug = require('gulp-pug');
	// var locals = require('src/locals.js');

	gulp.src('src/**/*.pug')
		.pipe(pug({
			'pretty': true
			// 'locals': locals
		}))
		.pipe(gulp.dest(html_dest)); // tell gulp our output folder
});

// Compiles .sass into .css
gulp.task('sass', function() {
	var sass = require('gulp-sass');

	gulp.src('src/sass/**.sass')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest(sass_dest));
});

//
gulp.task('build', ['pug', 'sass']);

// Monitors .pug and .sass
gulp.task('watch', function() {
	gulp.watch('src/**/*', ['build']);
});

//
gulp.task('default', ['watch']);

//
gulp.task('test', function() {
  	// place code for your default task here
	console.log("Hi, I'm Gulp!")
});
