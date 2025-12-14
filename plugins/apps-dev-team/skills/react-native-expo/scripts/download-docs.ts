#!/usr/bin/env npx ts-node
/**
 * React Native & Expo Documentation Downloader
 * 
 * Downloads and organizes documentation from:
 * - Expo SDK (docs.expo.dev)
 * - React Native (reactnative.dev)
 * 
 * Usage: npx ts-node download-docs.ts [--output <dir>] [--expo-only] [--rn-only]
 */

import * as fs from 'fs';
import * as path from 'path';
import * as https from 'https';

interface DocPage {
  title: string;
  url: string;
  category: string;
  content?: string;
}

interface DocConfig {
  baseUrl: string;
  pages: DocPage[];
}

// Expo SDK packages to download
const EXPO_SDK_PACKAGES = [
  'expo', 'accelerometer', 'apple-authentication', 'application', 'asset', 
  'audio', 'auth-session', 'av', 'background-task', 'barometer', 'battery',
  'blur-view', 'brightness', 'build-properties', 'calendar', 'camera',
  'cellular', 'checkbox', 'clipboard', 'constants', 'contacts', 'crypto',
  'dev-client', 'device', 'devicemotion', 'document-picker', 'filesystem',
  'font', 'gl-view', 'gyroscope', 'haptics', 'image', 'imagemanipulator',
  'imagepicker', 'intent-launcher', 'keep-awake', 'light-sensor', 'linear-gradient',
  'linking', 'live-photo', 'local-authentication', 'localization', 'location',
  'magnetometer', 'mail-composer', 'manifests', 'maps', 'media-library',
  'mesh-gradient', 'navigation-bar', 'network', 'notifications', 'pedometer',
  'print', 'router', 'screen-capture', 'screen-orientation', 'securestore',
  'sensors', 'sharing', 'sms', 'speech', 'splash-screen', 'sqlite',
  'status-bar', 'storereview', 'symbols', 'system-ui', 'task-manager',
  'tracking-transparency', 'updates', 'video', 'video-thumbnails', 'webbrowser'
];

// Expo guides and configuration
const EXPO_GUIDES = [
  { path: 'guides/overview', category: 'guides' },
  { path: 'develop/development-builds/introduction', category: 'development' },
  { path: 'develop/development-builds/create-a-build', category: 'development' },
  { path: 'router/introduction', category: 'router' },
  { path: 'router/layouts', category: 'router' },
  { path: 'router/navigating-pages', category: 'router' },
  { path: 'router/advanced/tabs', category: 'router' },
  { path: 'router/advanced/stack', category: 'router' },
  { path: 'router/advanced/drawer', category: 'router' },
  { path: 'router/advanced/nesting-navigators', category: 'router' },
  { path: 'router/advanced/modals', category: 'router' },
  { path: 'router/reference/typed-routes', category: 'router' },
  { path: 'versions/latest/config/app', category: 'config' },
  { path: 'versions/latest/config/metro', category: 'config' },
  { path: 'build/introduction', category: 'eas' },
  { path: 'build/setup', category: 'eas' },
  { path: 'build/eas-json', category: 'eas' },
  { path: 'submit/introduction', category: 'eas' },
  { path: 'eas-update/introduction', category: 'eas' },
  { path: 'workflow/configuration', category: 'workflow' },
  { path: 'workflow/prebuild', category: 'workflow' },
  { path: 'workflow/using-libraries', category: 'workflow' },
  { path: 'more/expo-cli', category: 'cli' },
];

// React Native core components and APIs
const REACT_NATIVE_PAGES = [
  // Core Components
  { path: 'view', category: 'components' },
  { path: 'text', category: 'components' },
  { path: 'image', category: 'components' },
  { path: 'textinput', category: 'components' },
  { path: 'scrollview', category: 'components' },
  { path: 'flatlist', category: 'components' },
  { path: 'sectionlist', category: 'components' },
  { path: 'button', category: 'components' },
  { path: 'switch', category: 'components' },
  { path: 'touchableopacity', category: 'components' },
  { path: 'touchablehighlight', category: 'components' },
  { path: 'pressable', category: 'components' },
  { path: 'modal', category: 'components' },
  { path: 'activityindicator', category: 'components' },
  { path: 'keyboardavoidingview', category: 'components' },
  { path: 'refreshcontrol', category: 'components' },
  { path: 'safeareaview', category: 'components' },
  { path: 'statusbar', category: 'components' },
  { path: 'virtualizedlist', category: 'components' },
  
  // APIs
  { path: 'animated', category: 'apis' },
  { path: 'alert', category: 'apis' },
  { path: 'appearance', category: 'apis' },
  { path: 'dimensions', category: 'apis' },
  { path: 'keyboard', category: 'apis' },
  { path: 'layoutanimation', category: 'apis' },
  { path: 'linking', category: 'apis' },
  { path: 'panresponder', category: 'apis' },
  { path: 'pixelratio', category: 'apis' },
  { path: 'platform', category: 'apis' },
  { path: 'platformcolor', category: 'apis' },
  { path: 'share', category: 'apis' },
  { path: 'stylesheet', category: 'apis' },
  { path: 'transforms', category: 'apis' },
  { path: 'usecolorscheme', category: 'apis' },
  { path: 'usewindowdimensions', category: 'apis' },
  { path: 'vibration', category: 'apis' },
  
  // Guides
  { path: 'getting-started', category: 'guides' },
  { path: 'intro-react-native-components', category: 'guides' },
  { path: 'handling-text-input', category: 'guides' },
  { path: 'handling-touches', category: 'guides' },
  { path: 'using-a-scrollview', category: 'guides' },
  { path: 'using-a-listview', category: 'guides' },
  { path: 'network', category: 'guides' },
  { path: 'style', category: 'guides' },
  { path: 'height-and-width', category: 'guides' },
  { path: 'flexbox', category: 'guides' },
  { path: 'images', category: 'guides' },
  { path: 'navigation', category: 'guides' },
  { path: 'animations', category: 'guides' },
  { path: 'gesture-responder-system', category: 'guides' },
  { path: 'javascript-environment', category: 'guides' },
  { path: 'timers', category: 'guides' },
  { path: 'performance', category: 'guides' },
  { path: 'debugging', category: 'guides' },
  { path: 'testing-overview', category: 'guides' },
  { path: 'typescript', category: 'guides' },
  { path: 'native-modules-intro', category: 'native' },
  { path: 'native-components-android', category: 'native' },
  { path: 'native-components-ios', category: 'native' },
  { path: 'turbo-native-modules-introduction', category: 'native' },
];

async function fetchPage(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => resolve(data));
      res.on('error', reject);
    }).on('error', reject);
  });
}

function extractMarkdownContent(html: string): string {
  // Simple extraction - in real usage you'd want a proper HTML parser
  // This extracts the main content and converts basic HTML to markdown
  let content = html
    // Remove script and style tags
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    // Convert headers
    .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '\n# $1\n')
    .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '\n## $1\n')
    .replace(/<h3[^>]*>(.*?)<\/h3>/gi, '\n### $1\n')
    .replace(/<h4[^>]*>(.*?)<\/h4>/gi, '\n#### $1\n')
    // Convert code blocks
    .replace(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/gi, '\n```\n$1\n```\n')
    .replace(/<code[^>]*>(.*?)<\/code>/gi, '`$1`')
    // Convert links
    .replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, '[$2]($1)')
    // Convert lists
    .replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n')
    // Convert paragraphs
    .replace(/<p[^>]*>(.*?)<\/p>/gi, '\n$1\n')
    // Remove remaining HTML tags
    .replace(/<[^>]+>/g, '')
    // Clean up entities
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    // Clean up whitespace
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  return content;
}

async function downloadExpoSDKDocs(outputDir: string): Promise<void> {
  const sdkDir = path.join(outputDir, 'expo-sdk');
  fs.mkdirSync(sdkDir, { recursive: true });

  console.log('Downloading Expo SDK documentation...');
  
  for (const pkg of EXPO_SDK_PACKAGES) {
    const url = `https://docs.expo.dev/versions/latest/sdk/${pkg}/`;
    console.log(`  Fetching: ${pkg}`);
    
    try {
      const html = await fetchPage(url);
      const content = extractMarkdownContent(html);
      const filename = path.join(sdkDir, `${pkg}.md`);
      fs.writeFileSync(filename, `# expo-${pkg}\n\nSource: ${url}\n\n${content}`);
    } catch (error) {
      console.error(`  Error fetching ${pkg}:`, error);
    }
    
    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}

async function downloadExpoGuides(outputDir: string): Promise<void> {
  const guidesDir = path.join(outputDir, 'expo-guides');
  fs.mkdirSync(guidesDir, { recursive: true });

  console.log('Downloading Expo guides...');
  
  for (const guide of EXPO_GUIDES) {
    const url = `https://docs.expo.dev/${guide.path}/`;
    const filename = guide.path.replace(/\//g, '-');
    console.log(`  Fetching: ${guide.path}`);
    
    try {
      const html = await fetchPage(url);
      const content = extractMarkdownContent(html);
      const filepath = path.join(guidesDir, `${filename}.md`);
      fs.writeFileSync(filepath, `# ${guide.path}\n\nCategory: ${guide.category}\nSource: ${url}\n\n${content}`);
    } catch (error) {
      console.error(`  Error fetching ${guide.path}:`, error);
    }
    
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}

async function downloadReactNativeDocs(outputDir: string): Promise<void> {
  const rnDir = path.join(outputDir, 'react-native');
  fs.mkdirSync(rnDir, { recursive: true });

  console.log('Downloading React Native documentation...');
  
  for (const page of REACT_NATIVE_PAGES) {
    const url = `https://reactnative.dev/docs/${page.path}`;
    console.log(`  Fetching: ${page.path}`);
    
    try {
      const html = await fetchPage(url);
      const content = extractMarkdownContent(html);
      const filepath = path.join(rnDir, `${page.category}-${page.path}.md`);
      fs.writeFileSync(filepath, `# ${page.path}\n\nCategory: ${page.category}\nSource: ${url}\n\n${content}`);
    } catch (error) {
      console.error(`  Error fetching ${page.path}:`, error);
    }
    
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}

async function createIndexFiles(outputDir: string): Promise<void> {
  // Create SDK index
  const sdkFiles = fs.readdirSync(path.join(outputDir, 'expo-sdk'));
  const sdkIndex = `# Expo SDK Reference Index

## Available Packages

${sdkFiles.map(f => `- [${f.replace('.md', '')}](./expo-sdk/${f})`).join('\n')}

## Quick Reference

### Most Common Packages
- expo-camera: Camera access and barcode scanning
- expo-image-picker: Select images/videos from library or camera
- expo-location: Geolocation and geocoding
- expo-notifications: Push and local notifications
- expo-file-system: File system access
- expo-secure-store: Encrypted key-value storage
- expo-auth-session: OAuth/OpenID authentication
- expo-router: File-based routing (recommended)
- expo-sqlite: SQLite database
- expo-av / expo-video: Audio and video playback
`;

  fs.writeFileSync(path.join(outputDir, 'EXPO-SDK-INDEX.md'), sdkIndex);

  // Create React Native index
  const rnFiles = fs.readdirSync(path.join(outputDir, 'react-native'));
  const components = rnFiles.filter(f => f.startsWith('components-'));
  const apis = rnFiles.filter(f => f.startsWith('apis-'));
  const guides = rnFiles.filter(f => f.startsWith('guides-'));

  const rnIndex = `# React Native Reference Index

## Core Components
${components.map(f => `- [${f.replace('components-', '').replace('.md', '')}](./react-native/${f})`).join('\n')}

## APIs
${apis.map(f => `- [${f.replace('apis-', '').replace('.md', '')}](./react-native/${f})`).join('\n')}

## Guides
${guides.map(f => `- [${f.replace('guides-', '').replace('.md', '')}](./react-native/${f})`).join('\n')}
`;

  fs.writeFileSync(path.join(outputDir, 'REACT-NATIVE-INDEX.md'), rnIndex);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const outputDir = args.includes('--output') 
    ? args[args.indexOf('--output') + 1] 
    : './docs';
  
  const expoOnly = args.includes('--expo-only');
  const rnOnly = args.includes('--rn-only');

  fs.mkdirSync(outputDir, { recursive: true });
  console.log(`Output directory: ${outputDir}`);

  if (!rnOnly) {
    await downloadExpoSDKDocs(outputDir);
    await downloadExpoGuides(outputDir);
  }

  if (!expoOnly) {
    await downloadReactNativeDocs(outputDir);
  }

  await createIndexFiles(outputDir);
  
  console.log('\nDocumentation download complete!');
  console.log(`Files saved to: ${outputDir}`);
}

main().catch(console.error);
