var fs = require('fs');
var gulp = require('gulp');

var build = 'html';

// Compiles .pug files into .html
gulp.task('pug', function() {
    var pug = require('gulp-pug');
    var locals = require('./src/locals.js');
    gulp.src('src/pug/*.pug')
        .pipe(pug({
            locals: locals
        }).on('error', console.log))
        .pipe(gulp.dest(build));
});

// Compiles .sass into .css
gulp.task('sass', function() {
    var sass = require('gulp-sass');
    gulp.src('src/sass/*.sass')
        .pipe(sass().on('error', sass.logError))
    	.pipe(gulp.dest(build + '/css/'));
});

// Copies bootstrap files into build
gulp.task('bootstrap', function() {
    gulp.src('src/static/bootstrap/*.css')
        .pipe(gulp.dest(build + '/css/'));
    gulp.src('src/static/bootstrap/*.js')
        .pipe(gulp.dest(build + '/js/'))
});

// Copies assets into build
gulp.task('assets', function() {
    gulp.src('src/static/assets/*')
        .pipe(gulp.dest(build + '/assets/'))
});

// Copy favicons into place
gulp.task('favicon', function() {
    console.log("Favicon stub!")
});

// Removes built files
gulp.task('clean', function() {
    var clean = require('gulp-clean');
    gulp.src('html/**', {read:false})
        .pipe(clean());
});

// Monitors .pug and .sass
gulp.task('watch', function() {
    gulp.watch('src/**', ['build']);
});

// Single time build of files
gulp.task('build', ['pug', 'sass', 'bootstrap', 'assets']);
gulp.task('default', ['build']);


gulp.task('repos', () => {
    repos.then(res => {
        console.log(res)
    })
});
