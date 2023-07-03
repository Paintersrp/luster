import { queueStoreFile } from '../queue/queueStore.js';
import { handleFunction } from '../utils/error.js';
import { capFirst } from '../utils/format.js';
import { getPaths } from '../utils/getPaths.js';
import { SyGen, SyLog } from '../utils/index.js';
import { validateName } from '../utils/validate.js';

/**
 * @description
 * Generate scaffolding for a Zustand store based on the provided store name.
 *
 * @param {string} storeName - The name of the store.
 * @throws {Error} If an error occurs during the generation process.
 * @returns {Promise<void>}
 * @async
 */
export async function generateStore(storeName) {
  await handleFunction(async () => {
    const validatedName = validateName(storeName);
    const formattedName = capFirst(validatedName);
    const lowercaseName = validatedName.toLowerCase();

    const generator = new SyGen();
    const paths = getPaths();

    await generator.ensureAndLogDir(paths.src.stores);
    await queueStoreFile(formattedName, lowercaseName, paths.src.stores, generator);

    const templatesUsed = await generator.generateQueue();
    SyLog.logStats(templatesUsed);
  });
}
