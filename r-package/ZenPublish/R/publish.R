#' @export
publish <- function() {

  # Get the document context.
  context <- rstudioapi::getSourceEditorContext()$path
  expr <- paste0("zen publish")
  result = tryCatch({
    system(expr, intern = FALSE)
  }, warning = function(war) {
    print(paste("MY_WARNING:  ", war))
  }, error = function(err) {
    print(paste("MY_WARNING:  ", err))
  }, finally = {
    print("Publish Document")
  })
}
