import fs from 'fs';
import glob from 'glob';
import matter from 'gray-matter';
import marked from 'marked';
import mkdirp from 'mkdirp';
import path from 'path';

// Copy the file to the output directory
const copyFile = (srcFilename, outFilename) => {
	const dir = path.dirname(outFilename);
	mkdirp.sync(dir);
	fs.copyFileSync(srcFilename, outFilename);
	console.log(`📝 Copied file to ${outFilename}`);
};

// Read the file, parse the front matter, and convert the markdown to HTML
const readFile = (filename) => {
	const rawFile = fs.readFileSync(filename, 'utf8');
	const parsed = matter(rawFile);
	const html = marked(parsed.content);
	return { ...parsed, html };
};

// Replace the placeholders in the template with the actual content
const templatize = (template, { date, title, content, smallDivs }) =>
	template
		.replace(/<!-- PUBLISH_DATE -->/g, date)
		.replace(/<!-- TITLE -->/g, title)
		.replace(/<!-- CONTENT -->/g, content)
		.replace(/<!-- SMALL_DIVS -->/g, smallDivs);

// Save the file to the output directory
const saveFile = (filename, contents) => {
	const dir = path.dirname(filename);
	mkdirp.sync(dir);
	fs.writeFileSync(filename, contents);
};

// Generate the output filename for HTML files based on the input filename
const getHtmlOutputFilename = (filename, outPath, subfolder = 'posts') => {
	const basename = path.basename(filename, path.extname(filename)); // Get the filename without extension
	const newfilename = basename + '.html';
	const outfile = path.join(outPath, subfolder, newfilename); // Save in subfolder in 'dist'
	return outfile;
};

// Generate small divs from numbered post files
const generateSmallDivs = (template, count, postsPath) => {
	let smallDivs = '';
	for (let i = 1; i <= count; i++) {
		const filename = path.join(postsPath, i + '.md');
		const file = readFile(filename);

// Process the file: read, templatize, and save
const processFile = (filename, template, outPath,  smallDivTemplate, smallDivCount) => {
	const file = readFile(filename);
	const outfilename = getHtmlOutputFilename(filename, outPath);
	const smallDivs = generateSmallDivs(smallDivTemplate, smallDivCount, postsPath);
	const templatized = templatize(template, {
		date: file.data.date,
		title: file.data.title,
		content: file.html,
		smallDivs: smallDivs
	});
	saveFile(outfilename, templatized);
	console.log(`📝 Processed file: ${outfilename}`);
};

// Generate the index page
const generateIndexPage = (template, outPath, smallDivTemplate, smallDivCount) => {
	const postDivs = generateSmallDivs(smallDivTemplate, smallDivCount, postsPath);
	const indexContent = templatize(template, {
		date: '',
		title: 'Welcome to the Blog',
		content: '',
		postDivs: postDivs
	});
	const indexPath = path.join(outPath, 'index.html');
	saveFile(indexPath, indexContent);
	console.log(`📝 Generated index page: ${indexPath}`);
};

// Main function
const main = () => {
	// Read the template and the markdown files
	const srcPath = path.resolve('src');
	// Create/resolve the output directory
	const outPath = path.resolve('dist');
	// Read the main template
	const template = fs.readFileSync(path.join(srcPath, 'template.html'), 'utf8');
	// Read the small div template
	const smallDivTemplate = fs.readFileSync(path.join(srcPath, 'postTemplate.html'), 'utf8');
	// Get all the markdown files from 'posts' subfolder
	const filenames = glob.sync(srcPath + '/pages/posts/**/*.md');

	// Generate the index page
	generateIndexPage(template, outPath, smallDivTemplate, smallDivCount);

	// Process the markdown files
	filenames.forEach((filename) => {
		processFile(filename, template, outPath, smallDivTemplate, smallDivCount);
	});

	// Get all the CSS files
	const cssFiles = glob.sync(srcPath + '/css/**/*.css');
	console.log('📝 Copying CSS files', cssFiles);

	// Copy the CSS files
	cssFiles.forEach((filename) => {
		const outfilename = path.join(outPath, 'css', path.basename(filename));
		copyFile(filename, outfilename);
	});

	// Get all the media files
	const mediaFiles = glob.sync(srcPath + '/pages/media/**/*.*');
	console.log('📝 Copying media files', mediaFiles);

	// Copy the media files
	mediaFiles.forEach((filename) => {
		const outfilename = path.join(outPath, 'media', path.basename(filename));
		console.log('Copying', filename, 'to', outfilename);
		copyFile(filename, outfilename);
	});
	console.log('Output path: ' + outPath);
};

main();


