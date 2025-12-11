# CSS Troubleshooting Specification: Physical AI & Humanoid Robotics Textbook

## Overview

This specification outlines systematic steps to diagnose and resolve CSS-related issues in the Physical AI & Humanoid Robotics Textbook Docusaurus project. The document follows the development workflow principles and technical standards established in the main project specifications.

## Issue Diagnosis

### Symptom: CSS not working
- Custom styles from src/css/custom.css are not being applied to the site
- Default Docusaurus/Infima styling may be present but customizations are missing
- Potential configuration, build, or path issues

## Troubleshooting Steps

### 1. Configuration Verification
**Objective**: Confirm CSS file is correctly referenced in docusaurus.config.js

**Actions**:
1. Verify the customCss path in your theme configuration
2. Ensure the path matches the actual file location
3. Check for syntax errors in the configuration file

### 2. File Structure Verification
**Objective**: Confirm the CSS file exists in the correct location with appropriate content

**Actions**:
1. Verify file exists at src/css/custom.css
2. Check that CSS syntax is valid
3. Confirm the file is not empty or corrupted

### 3. Cache and Build Issues
**Objective**: Address common caching problems that prevent CSS changes from appearing

**Actions**:
1. Clear Docusaurus cache with `npm run clear`
2. Rebuild the site with `npm run build`
3. Restart the development server with `npm run start`

### 4. Browser Cache Issues
**Objective**: Ensure browser is not displaying cached versions without CSS changes

**Actions**:
1. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Test in an incognito/private browsing window

### 5. Path Resolution Issues
**Objective**: Ensure file paths are correctly resolved by the module system

**Actions**:
1. Try using absolute path imports if relative path fails
2. Verify the file path in the theme configuration
3. Check for any typos in the path reference

## Implementation Plan

### Phase 1: Verification (Immediate)
1. Confirm the existence of src/css/custom.css file
2. Validate the path is correctly referenced in docusaurus.config.js
3. Check for any syntax errors in the CSS file

### Phase 2: Clearing (Next Step)
1. Clear Docusaurus cache with `npx docusaurus clear`
2. Clear browser cache
3. Rebuild the project

### Phase 3: Testing (After Clearing)
1. Start development server with `npx docusaurus start`
2. Test in different browsers
3. Verify custom styles are applied

### Phase 4: Alternative Approach (If Previous Phases Fail)
1. Create a new CSS file at a different location
2. Update configuration to use new path
3. Test if the issue is path-specific

## Expected Outcomes

- Custom CSS styles defined in src/css/custom.css should be properly applied to the site
- Color schemes and other customizations should be visible and functional
- Both light and dark mode customizations should work correctly

## Success Criteria

- Visiting the site shows custom colors (e.g., #2e8555 as primary color)
- Custom styles override default Infima styles
- CSS changes are reflected after saving the custom.css file
- No build errors related to CSS loading appear in the console

## Rollback Plan

If troubleshooting creates new issues:
1. Revert docusaurus.config.js to the previous working state
2. Restore any modified CSS files from backup
3. Reinstall project dependencies if needed

## Prevention Measures

For future development:
1. Always follow the established development workflow when making CSS changes
2. Test CSS changes in multiple browsers
3. Use the project's established CSS structure and conventions
4. Implement CSS changes incrementally to isolate issues