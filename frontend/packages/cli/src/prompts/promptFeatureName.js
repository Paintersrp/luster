import fs from 'fs-extra';
import inquirer from 'inquirer';

import { FEATURES_DIR } from '../../config.js';
import { SyLog } from '../utils/SyLog.js';

/**
 * Prompts the user to choose a feature name from the existing feature directories.
 * @returns {Promise<string>} - The selected feature name.
 */
export async function promptFeatureName() {
  const featuresExists = await fs.pathExists(FEATURES_DIR);
  if (!featuresExists) {
    SyLog.error('The features directory does not exist.');
  }

  const featureFolders = await fs.readdir(FEATURES_DIR);
  if (featureFolders.length === 0) {
    SyLog.error('There are no subdirectories in the features directory.');
  }

  return inquirer
    .prompt([
      {
        type: 'list',
        name: 'featureName',
        message: 'Choose a feature:',
        choices: featureFolders,
      },
    ])
    .then((answers) => answers.featureName);
}