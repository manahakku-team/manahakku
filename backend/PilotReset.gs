/**
 * Mana Hakku · start the pilot with a clean register.
 *
 * Moves every test row out of Reports, Flags, Suggestions and Usage into new "Archive" tabs in the same
 * spreadsheet. Nothing is deleted: the archive tabs keep every row exactly as it was, so it can be copied back.
 *
 * How to use (once, just before the pilot starts):
 *   1. In the Apps Script editor, add a new script file (+ › Script), name it PilotReset, paste this file, save.
 *   2. Choose  previewTestData  in the function list and press Run. Read the log: it only counts rows.
 *   3. Choose  archiveTestDataForPilot  and press Run. Approve the permission prompt if Google asks.
 * No new deployment is needed; the app keeps working throughout.
 */
const PILOT_TABS = ['Reports', 'Flags', 'Suggestions', 'Usage'];

function previewTestData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  PILOT_TABS.forEach(name => {
    const sh = ss.getSheetByName(name);
    Logger.log(name + ': ' + (sh ? Math.max(0, sh.getLastRow() - 1) : 0) + ' rows would be archived');
  });
}

function archiveTestDataForPilot() {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);   // no report can be saved halfway through the move
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const stamp = Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyyy-MM-dd');
    PILOT_TABS.forEach(name => {
      const sh = ss.getSheetByName(name);
      if (!sh || sh.getLastRow() < 2) { Logger.log(name + ': nothing to archive'); return; }
      const rows = sh.getLastRow() - 1, cols = sh.getLastColumn();
      const all = sh.getRange(1, 1, rows + 1, cols).getValues();
      const arch = ss.insertSheet('Archive ' + stamp + ' · ' + name);
      arch.getRange(1, 1, all.length, cols).setValues(all);
      arch.setFrozenRows(1);
      if (arch.getRange(arch.getLastRow(), 1, 1, cols).getValues()[0].join('') !== all[all.length - 1].join('')) {
        throw new Error(name + ': copy check failed, nothing was removed');
      }
      sh.deleteRows(2, rows);
      Logger.log(name + ': ' + rows + ' rows moved to "' + arch.getName() + '"');
    });
    Logger.log('Done. The register is empty and ready for the pilot.');
  } finally {
    lock.releaseLock();
  }
}
