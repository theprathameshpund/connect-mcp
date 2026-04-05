function log(message) {
  console.log(message);
}

function success(message) {
  console.log("✅ " + message);
}

function error(message) {
  console.log("❌ " + message);
}

function warn(message) {
  console.log("⚠️ " + message);
}

function info(message) {
  console.log("ℹ️ " + message);
}

module.exports = {
  log,
  success,
  error,
  warn,
  info
};